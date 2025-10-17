import contextlib
from datetime import UTC, datetime
import json
from typing import Any, List, Dict, Optional, Type, get_args, get_origin
from pydantic import (
    BaseModel,
    Field,
    constr,
    conint,
    confloat,
    StrictStr,
    StrictInt,
    StrictFloat,
    StrictBool,
    StringConstraints,
)
from pydantic_core import PydanticUndefined
import stix2.properties as stixprops
import inspect
from stix2 import ExternalReference, IPv4Address
import stix2
import stix2.properties
from typing import Literal

import stix2.utils


_UUID_RE = r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"


def _reference_regex_from_valid_types(valid_types):
    if isinstance(valid_types, str):
        valid_types = [valid_types]
    types_pattern = "|".join(valid_types)
    return rf"^({types_pattern})--{_UUID_RE}$"


class PydanticMixin:
    """
    Mixin for STIX property classes, adding a .pydantic_type attribute,
    .pydantic_field for use in Pydantic models, and supports descriptions.
    """

    def __init__(self, *args, description: str = None, examples=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._description = description
        self._field_name = None
        self._containing_type = None
        self._examples = examples

    @property
    def pydantic_type(self):
        if isinstance(self, stixprops.Property) and hasattr(self, '_fixed_value'):
            print(self._field_name, self._fixed_value, type(self))
            return Literal[self._fixed_value]
        if isinstance(self, stixprops.ListProperty):
            contained = getattr(self, "contained", None)
            return List[_make_pydantic_property(contained).pydantic_type]

        if isinstance(self, stixprops.IDProperty):
            self.required = True
            regex = _reference_regex_from_valid_types(self._containing_type)
            return constr(pattern=regex)

        if isinstance(self, stixprops.TypeProperty):
            self.required = True
            return Literal[self._containing_type]

        if isinstance(self, stixprops.EmbeddedObjectProperty):
            if hasattr(self.type, "PydanticModel"):
                return self.type.PydanticModel
            return dict

        if isinstance(
            self, (stixprops.ObservableProperty, stixprops.STIXObjectProperty)
        ):
            return dict

        if isinstance(self, stixprops.ReferenceProperty):
            if getattr(self, "auth_type", None) == getattr(
                stixprops.ReferenceProperty, "_WHITELIST", 0
            ):
                valid_types = list(getattr(self, "specifics", []))
                regex = _reference_regex_from_valid_types(valid_types)
                if regex:
                    return constr(pattern=regex)
            return StrictStr

        if hasattr(stixprops, "ExternalReferenceProperty") and isinstance(
            self, stixprops.ExternalReferenceProperty
        ):
            if hasattr(self, "type") and hasattr(self.type, "PydanticModel"):
                return self.type.PydanticModel
            return dict

        if isinstance(self, stixprops.EnumProperty):
            return Literal[tuple(self.allowed)]

        _PROPERTY_TYPE_MAP = {
            stixprops.StringProperty: StrictStr,
            stixprops.IntegerProperty: StrictInt,
            stixprops.FloatProperty: StrictFloat,
            stixprops.BooleanProperty: StrictBool,
            stixprops.DictionaryProperty: dict,
            stixprops.OpenVocabProperty: StrictStr,
            stixprops.ObjectReferenceProperty: StrictStr,
            stixprops.PatternProperty: StrictStr,
            stixprops.HexProperty: StrictStr,
            stixprops.BinaryProperty: StrictStr,
            stixprops.SelectorProperty: StrictStr,
            stixprops.IDProperty: StrictStr,
            stixprops.TypeProperty: StrictStr,
            stixprops.TimestampProperty: str,
            stixprops.HashesProperty: dict,
            stixprops.ExtensionsProperty: dict,
        }
        for stix_cls, ptype in _PROPERTY_TYPE_MAP.items():
            if isinstance(self, stix_cls):
                return ptype

        return Any

    @property
    def pydantic_field(self):
        default = ...
        # required
        # constraints for int/float
        constraints = {}
        if isinstance(self, stixprops.IntegerProperty):
            if getattr(self, "min", None) is not None:
                constraints["ge"] = self.min
            if getattr(self, "max", None) is not None:
                constraints["le"] = self.max
        if isinstance(self, stixprops.FloatProperty):
            if getattr(self, "min", None) is not None:
                constraints["ge"] = self.min
            if getattr(self, "max", None) is not None:
                constraints["le"] = self.max
        # apply constraints
        examples=getattr(self, 'examples', None) or []
        kwargs = dict()
        typ = self.pydantic_type
        print(typ, self._field_name)
        if not getattr(self, "required", None):
            typ = Optional[self.pydantic_type]
            kwargs.update(default=PydanticUndefined)
        if _description := getattr(self, "_description", None):
            kwargs.update(description=_description)
        if default_fn := getattr(self, "default", None):
            kwargs.update(default_factory=default_fn)
            kwargs.pop("default", None)
            with contextlib.suppress(Exception):
                examples.append(transform_examples(default_fn()))
        if examples:
            kwargs.update(examples=examples)

        if constraints:
            if inspect.isclass(typ) and issubclass(typ, int):
                typ = conint(**constraints)
            elif inspect.isclass(typ) and issubclass(typ, float):
                typ = confloat(**constraints)

        return (typ, Field(**kwargs))

    @staticmethod
    def make_name(base_cls: Type):
        print(base_cls.__name__, base_cls.__qualname__)
        name = base_cls.__qualname__
        if not name.startswith("Pydantic"):
            name = "Pydantic" + base_cls.__name__
        return name


REGISTRY: dict[str, PydanticMixin] = {}


# Dynamically create Pydantic*Property classes
def _make_pydantic_property_class(base_cls: Type):
    class _PydanticProperty(PydanticMixin, base_cls):
        def __init__(self, *args, description: str = None, **kwargs):
            super().__init__(*args, description=description, **kwargs)

    _PydanticProperty.__qualname__ = PydanticMixin.make_name(base_cls)
    REGISTRY.update({_PydanticProperty.__qualname__: _PydanticProperty})
    print(REGISTRY)
    return _PydanticProperty


def _make_pydantic_property(prop_instance):
    if not isinstance(prop_instance, stixprops.Property):
        return prop_instance
    typ = REGISTRY[PydanticMixin.make_name(prop_instance.__class__)]
    f = typ.__new__(typ)
    f.__dict__.update(prop_instance.__dict__)
    return f


S2EStringProperty = _make_pydantic_property_class(stixprops.StringProperty)
S2EIntegerProperty = _make_pydantic_property_class(stixprops.IntegerProperty)
S2EFloatProperty = _make_pydantic_property_class(stixprops.FloatProperty)
S2EBooleanProperty = _make_pydantic_property_class(stixprops.BooleanProperty)
S2EDictionaryProperty = _make_pydantic_property_class(stixprops.DictionaryProperty)
S2EEnumProperty = _make_pydantic_property_class(stixprops.EnumProperty)
S2EOpenVocabProperty = _make_pydantic_property_class(stixprops.OpenVocabProperty)
S2EObjectReferenceProperty = _make_pydantic_property_class(
    stixprops.ObjectReferenceProperty
)
S2EPatternProperty = _make_pydantic_property_class(stixprops.PatternProperty)
S2EHexProperty = _make_pydantic_property_class(stixprops.HexProperty)
S2EBinaryProperty = _make_pydantic_property_class(stixprops.BinaryProperty)
S2ESelectorProperty = _make_pydantic_property_class(stixprops.SelectorProperty)
S2EIDProperty = _make_pydantic_property_class(stixprops.IDProperty)
S2ETypeProperty = _make_pydantic_property_class(stixprops.TypeProperty)
S2ETimestampProperty = _make_pydantic_property_class(stixprops.TimestampProperty)
S2EHashesProperty = _make_pydantic_property_class(stixprops.HashesProperty)
S2EExtensionsProperty = _make_pydantic_property_class(stixprops.ExtensionsProperty)
S2EReferenceProperty = _make_pydantic_property_class(stixprops.ReferenceProperty)
if hasattr(stixprops, "ExternalReferenceProperty"):
    PydanticExternalReferenceProperty = _make_pydantic_property_class(
        stixprops.ExternalReferenceProperty
    )
S2EListProperty = _make_pydantic_property_class(stixprops.ListProperty)
S2EEmbeddedObjectProperty = _make_pydantic_property_class(
    stixprops.EmbeddedObjectProperty
)
S2EObservableProperty = _make_pydantic_property_class(stixprops.ObservableProperty)
S2ESTIXObjectProperty = _make_pydantic_property_class(stixprops.STIXObjectProperty)


from typing import Any, Dict, Type
from pydantic import BaseModel, create_model
import stix2.properties as stixprops
import inspect

def auto_model(cls: Type[Any]) -> Type[BaseModel]:
    """
    Class decorator that creates a Pydantic model from a class using Pydantic*Property fields.
    Usage:
        @auto_model
        class MyModel:
            name = PydanticStringProperty(required=True)
            age = PydanticIntegerProperty(default=30)
        # MyModel is now a Pydantic model!
    """
    annotations = dict(getattr(cls, "__annotations__", {}))

    for k, v in getattr(cls, "_properties", {}).items():
        if k not in cls.__dict__:
            # v.__class__ = PydanticMixin
            # setattr(cls, k, v)
            setattr(cls, k, _make_pydantic_property(v))

    fields = {}
    value: PydanticMixin
    for attr, value in list(cls.__dict__.items()):
        if not isinstance(value, (stixprops.Property, stix2.base._STIXBase)):
            continue
        value._containing_type = cls._type
        if hasattr(value, "pydantic_type"):
            annotations[attr] = value.pydantic_type
            value._field_name = attr
            typ, default = value.pydantic_field
            if default is ...:
                fields[attr] = (annotations[attr], ...)
            else:
                fields[attr] = (annotations[attr], default)
    # Set __annotations__ so that help(), etc. work properly
    cls.__annotations__ = annotations
    # Create and return the Pydantic model
    model = create_model(cls.__name__, **fields, __base__=BaseModel)
    model.__doc__ = cls.__doc__
    model.stix_schema = model.model_json_schema(mode="validation")
    model.stix_schema["$schema"] = "https://json-schema.org/draft/2020-12/schema"
    return model


def transform_examples(obj):
    if obj == stix2.utils.NOW:
        obj = datetime(2020, 1, 1, tzinfo=UTC)
    return obj

def make_schema(model):
    pass

from stix2 import CustomObservable
from stix2extensions._extensions import bank_account_ExtensionDefinitionSMO
_type = 'bank-account2'
@CustomObservable(_type, [
    ('type', S2ETypeProperty(_type, spec_version='2.1')),
    ('spec_version', S2EStringProperty(fixed='2.1')),
    ('id', S2EIDProperty(_type, spec_version='2.1')),
    ('country_ref', S2EReferenceProperty(valid_types='location', spec_version='2.1')),
    ('currency', S2EStringProperty()),
    ('bank', S2EStringProperty()),
    ('issuer_ref', S2EReferenceProperty(valid_types='identity', spec_version='2.1')),
    ('holder_ref', S2EReferenceProperty(valid_types='identity', spec_version='2.1')),
    ('account_number', S2EStringProperty()),
    ('iban', S2EStringProperty(required=True, description="Use IBAN Number")),
    ('bic', S2EStringProperty()),
    # ('extensions', ExtensionsProperty(spec_version='2.1'))
],  id_contrib_props=['iban', 'account_number', 'country_ref'])
class BankAccount(object):
    """
    This is a rteprtssjanajnshkjas of a abaopfjas  ;ldfaksa
    """
    with_extension = bank_account_ExtensionDefinitionSMO
    at_least_one_property = ['iban', 'account_number']

    def _check_object_constraints(self):
        self._check_at_least_one_property(self.at_least_one_property)

# print(MySTIXObject.model_json_schema(mode="validation"))
print(json.dumps(auto_model(stix2.Report).stix_schema))

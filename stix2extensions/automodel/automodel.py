import contextlib
from datetime import UTC, datetime
import json
from pydantic_core import PydanticUndefined
import stix2
from stix2.properties import Property
import stix2.properties as stixprops
from stix2.v21.base import _STIXBase
import stix2.utils
from typing import Literal, List, Any, Optional, Type, TYPE_CHECKING
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
    create_model,
)

from .definitions import ExtensionDict, _reference_regex_from_valid_types


class S2EProperty:
    field_name = ""
    parent_type = ""

    def __init__(self, property, description=None, examples=None, title=None):
        self.description = description
        self.examples = examples
        self.title = title
        self.property: Property = property

if TYPE_CHECKING:
    class ExtendedProperty(Property):
        _s2e_properties: S2EProperty = None


def pydantic_type(property: 'ExtendedProperty'):
    if not hasattr(property, "_s2e_properties"):
        extend_property(property)

    if isinstance(property, stixprops.ListProperty):
        contained = getattr(property, "contained", None)
        return List[pydantic_type(extend_property(contained))]

    if isinstance(property, stixprops.IDProperty):
        property.required = True
        regex = _reference_regex_from_valid_types(property._s2e_properties.parent_type)
        return constr(pattern=regex)

    if isinstance(property, stixprops.TypeProperty):
        property.required = True
        return Literal[property._s2e_properties.parent_type]

    if isinstance(property, stixprops.EmbeddedObjectProperty):
        if hasattr(property.type, "PydanticModel"):
            return property.type.PydanticModel
        return dict

    if isinstance(
        property, (stixprops.ObservableProperty, stixprops.STIXObjectProperty)
    ):
        return dict

    if isinstance(property, stixprops.ReferenceProperty):
        if getattr(property, "auth_type", None) == getattr(
            stixprops.ReferenceProperty, "_WHITELIST", 0
        ):
            valid_types = list(getattr(property, "specifics", []))
            regex = _reference_regex_from_valid_types(valid_types)
            if regex:
                return constr(pattern=regex)
        return StrictStr

    if hasattr(stixprops, "ExternalReferenceProperty") and isinstance(
        property, stixprops.ExternalReferenceProperty
    ):
        if hasattr(property, "type") and hasattr(property.type, "PydanticModel"):
            return property.type.PydanticModel
        return dict

    if isinstance(property, stixprops.EnumProperty):
        return Literal[tuple(property.allowed)]
    
    if isinstance(property, (stixprops.IntegerProperty, stixprops.FloatProperty)):
        constraints = {}
        if getattr(property, "min", None) is not None:
            constraints["ge"] = property.min
        if getattr(property, "max", None) is not None:
            constraints["le"] = property.max
        return confloat(**constraints) if isinstance(property, stixprops.FloatProperty) else conint(**constraints)
    
    if isinstance(property, stixprops.OpenVocabProperty) and hasattr(property, 'allowed'):
        rv = StrictStr
        if hasattr(property, 'allowed'):
            rv |= Literal[tuple(property.allowed)]
        return rv
        

    
    if isinstance(property, stixprops.Property) and hasattr(property, "_fixed_value"):
        return Literal[property._fixed_value]

    _PROPERTY_TYPE_MAP = {
        stixprops.StringProperty: StrictStr,
        stixprops.BooleanProperty: StrictBool,
        # stixprops.OpenVocabProperty: StrictStr,
        stixprops.ObjectReferenceProperty: StrictStr,
        stixprops.PatternProperty: StrictStr,
        stixprops.HexProperty: constr(pattern=r'^[0-9a-fA-F]+$'),
        stixprops.BinaryProperty: StrictStr,
        stixprops.SelectorProperty: constr(pattern=stixprops.SELECTOR_REGEX.pattern),
        stixprops.IDProperty: StrictStr,
        stixprops.TypeProperty: StrictStr,
        stixprops.TimestampProperty: datetime,
        stixprops.HashesProperty: dict,
        stixprops.ExtensionsProperty: ExtensionDict,
        stixprops.DictionaryProperty: dict,
    }
    for stix_cls, ptype in _PROPERTY_TYPE_MAP.items():
        if isinstance(property, stix_cls):
            return ptype

    return Any

def transform_examples(obj):
    if obj == stix2.utils.NOW:
        obj = datetime(2020, 1, 1, tzinfo=UTC)
    return obj

def pydantic_field(property: 'ExtendedProperty'):
        typ = pydantic_type(property)
        examples=getattr(property, 'examples', None) or []
        kwargs = dict()
        if not getattr(property, "required", None):
            typ = Optional[typ]
            kwargs.update(default=None)

        if _description := property._s2e_properties.description:
            kwargs.update(description=_description)

        kwargs.update(title=property._s2e_properties.title)

        if default_fn := getattr(property, "default", None):
            kwargs.update(default_factory=default_fn)
            kwargs.pop("default", None)
            with contextlib.suppress(Exception):
                examples.append(transform_examples(default_fn()))
        if getattr(property, "required", None):
            kwargs.pop('default_factory', None)
        if examples:
            kwargs.update(examples=examples)
        return typ, Field(**kwargs)


def extend_property(property: 'Property|ExtendedProperty', description=None, examples=None, title=None):
    if hasattr(property, '_s2e_properties'):
        return property
    property._s2e_properties = S2EProperty(
        property, description=description, examples=examples, title=title
    )
    return property


def auto_model(cls: Type[_STIXBase]) -> Type[BaseModel]:
    annotations = dict(getattr(cls, "__annotations__", {}))

    fields = {}
    value: 'ExtendedProperty'
    for attr, value in list(cls._properties.items()):
        if attr == 'first_name':
            pass
        cls._properties[attr] = extend_property(value)
        value._s2e_properties.parent_type = cls._type
        fields[attr] = pydantic_field(value)
        annotations[attr] = fields[attr][0]
    # print(fields, annotations)
    # Set __annotations__ so that help(), etc. work properly
    cls.__annotations__ = annotations
    # Create and return the Pydantic model
    model = create_model(cls.__name__, **fields, __base__=BaseModel)
    model.__doc__ = cls.__doc__
    model.stix_schema = model.model_json_schema(mode="validation")
    model.stix_schema["$schema"] = "https://json-schema.org/draft/2020-12/schema"
    return model
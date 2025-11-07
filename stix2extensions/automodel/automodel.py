import contextlib
from datetime import UTC, datetime
from enum import EnumType
import uuid
import stix2
from stix2.properties import Property
import stix2.properties as stixprops
from stix2.registry import class_for_type
from pydantic.json_schema import SkipJsonSchema

from stix2.v21.base import _STIXBase, _Extension
import stix2.utils
from typing import Annotated, ClassVar, Literal, List, Any, Optional, Type, TYPE_CHECKING
from pydantic import (
    BaseModel,
    Field,
    constr,
    conint,
    confloat,
    StrictStr,
    StrictBool,
    StringConstraints,
    create_model,
)

from .definitions import (
    STIX_ID_RE,
    ExtensionDict,
    Gen,
    Timestamp,
    _reference_regex_from_valid_types,
    get_properties,
)

namespace = uuid.UUID("1abb62b9-e513-5f55-8e73-8f6d7b55c237")

### dogesec

DOGESEC_IDENTITY_REF = "identity--" + str(uuid.uuid5(namespace, f"dogesec"))
CONST_CREATED = datetime(2020, 1, 1, tzinfo=UTC)
schema_base = (
    "https://raw.githubusercontent.com/muchdogesec/stix2extensions/main/schemas/"
)

### mitre TLP:CLEAR and stix4doge

S2E_MARKING_REFS = [
    "marking-definition--94868c89-83c2-464b-929b-a1a8aa3c8487",  # this is TLP:CLEAR
    "marking-definition--" + str(uuid.uuid5(namespace, f"stix2extensions")),  #
]


class S2EProperty:
    field_name = ""
    parent_type = ""

    def __init__(self, property, description=None, examples=None, title=None):
        self.description = description
        self.examples = examples
        self.title = title
        self.property: Property = property

    def add_example(self, *examples):
        self.examples = self.examples or []
        self.examples.extend(examples)


AUTOMODEL_REGISTRY: list[Type["ExtendedStixType"]] = []

if TYPE_CHECKING:

    class ExtendedProperty(Property):
        _s2e_properties: S2EProperty = None


class ExtensionType(object):
    name: str
    description: str | None
    extension_version: str = "1.0"
    extension_modified: datetime | str = None
    extension_created: datetime | str = CONST_CREATED
    base_schema: str = None


class ExtendedStixType(_STIXBase, ExtensionType):
    pydantic_model: BaseModel
    schema: dict
    extension_definition: stix2.ExtensionDefinition
    with_extension: Type["_Extension"]
    _properties: ClassVar[dict[str, Property]]



def pydantic_type(property: "ExtendedProperty"):
    if not hasattr(property, "_s2e_properties"):
        extend_property(property)

    if isinstance(property, stixprops.ListProperty):
        contained = getattr(property, "contained", None)
        return List[pydantic_type(extend_property(contained))]

    if isinstance(property, stixprops.IDProperty):
        property.required = True
        regex = _reference_regex_from_valid_types(property._s2e_properties.parent_type)
        property._s2e_properties.add_example(
            property._s2e_properties.parent_type
            + "--"
            + str(
                uuid.uuid5(namespace, property._s2e_properties.parent_type + "example")
            )
        )
        return Annotated[
            str,
            StringConstraints(pattern=regex),
            Field(
                examples=[
                    property._s2e_properties.parent_type
                    + "--"
                    + str(
                        uuid.uuid5(
                            namespace, property._s2e_properties.parent_type + str(i)
                        )
                    )
                    for i in range(3)
                ]
            ),
        ]

    if isinstance(property, stixprops.TypeProperty):
        property.required = True
        return Literal[property._s2e_properties.parent_type]

    if isinstance(property, stixprops.EmbeddedObjectProperty):
        if hasattr(property.type, "pydantic_model") or _STIXBase in property.type.mro():
            return auto_model(property.type).pydantic_model
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
                return Annotated[
                    str,
                    StringConstraints(pattern=regex),
                    Field(
                        examples=[
                            _t + "--" + str(uuid.uuid5(namespace, _t))
                            for _t in valid_types
                        ]
                    ),
                ]
        else:
            return Annotated[str, StringConstraints(pattern=STIX_ID_RE)]

    if hasattr(stixprops, "ExternalReferenceProperty") and isinstance(
        property, stixprops.ExternalReferenceProperty
    ):
        return dict

    if isinstance(property, stixprops.EnumProperty):
        return make_enum(property.allowed)

    if isinstance(property, (stixprops.IntegerProperty, stixprops.FloatProperty)):
        constraints = {}
        if getattr(property, "min", None) is not None:
            constraints["ge"] = property.min
        if getattr(property, "max", None) is not None:
            constraints["le"] = property.max
        return (
            confloat(**constraints)
            if isinstance(property, stixprops.FloatProperty)
            else conint(**constraints)
        )

    if isinstance(property, stixprops.OpenVocabProperty) and hasattr(
        property, "allowed"
    ):
        if hasattr(property, "allowed"):
            return make_enum(property.allowed) | StrictStr
        return StrictStr

    if isinstance(property, stixprops.Property) and hasattr(property, "_fixed_value"):
        return Literal[property._fixed_value]

    _PROPERTY_TYPE_MAP = {
        stixprops.StringProperty: StrictStr,
        stixprops.BooleanProperty: StrictBool,
        # stixprops.OpenVocabProperty: StrictStr,
        stixprops.ObjectReferenceProperty: StrictStr,
        stixprops.PatternProperty: StrictStr,
        stixprops.HexProperty: constr(pattern=r"^[0-9a-fA-F]+$"),
        stixprops.BinaryProperty: StrictStr,
        stixprops.SelectorProperty: constr(pattern=stixprops.SELECTOR_REGEX.pattern),
        stixprops.IDProperty: StrictStr,
        stixprops.TypeProperty: StrictStr,
        stixprops.TimestampProperty: Timestamp,
        stixprops.HashesProperty: dict,
        stixprops.ExtensionsProperty: ExtensionDict,
        stixprops.DictionaryProperty: dict,
    }
    for stix_cls, ptype in _PROPERTY_TYPE_MAP.items():
        if isinstance(property, stix_cls):
            return ptype

    return Any


def make_enum(lst: list | EnumType):
    if isinstance(lst, EnumType):
        return lst
    return Literal[tuple(lst)]


def schema_remove_default(s):
    if s.get("default", 1) == None:
        del s["default"]


def transform_examples(obj):
    if obj == stix2.utils.NOW:
        obj = datetime(2020, 1, 1, tzinfo=UTC)
    return obj


def pydantic_field(property: "ExtendedProperty"):
    typ = pydantic_type(property)
    examples = property._s2e_properties.examples or []
    kwargs = dict()
    if not getattr(property, "required", None):
        typ = typ | SkipJsonSchema[None]
        kwargs.update(default=None, json_schema_extra=schema_remove_default)

    if _description := property._s2e_properties.description:
        kwargs.update(description=_description)

    kwargs.update(title=property._s2e_properties.title)

    if default_fn := getattr(property, "default", None):
        kwargs.update(default_factory=default_fn)
        kwargs.pop("default", None)
        with contextlib.suppress(Exception):
            examples.append(transform_examples(default_fn()))
    if getattr(property, "required", None):
        kwargs.pop("default_factory", None)
    if examples:
        kwargs.update(examples=examples)
    return typ, Field(**kwargs)


def extend_property(
    property: "Property|ExtendedProperty", description=None, examples=None, title=None
):
    if hasattr(property, "_s2e_properties"):
        return property
    property._s2e_properties = S2EProperty(
        property, description=description, examples=examples, title=title
    )
    return property


def get_extension(cls: Type[ExtendedStixType], _extension_type):
    extension_name = cls.extension_definition["id"]
    NameExtension = class_for_type(cls.extension_definition["id"], "2.1", "extensions")
    if not NameExtension:

        @stix2.CustomExtension(type=extension_name, properties={})
        class NameExtension:
            extension_type = _extension_type

    return NameExtension


def auto_model(cls: Type[ExtendedStixType]):
    if cls in AUTOMODEL_REGISTRY:
        return cls
    annotations = dict(getattr(cls, "__annotations__", {}))
    model_type = getattr(cls, "_type", None)

    fields = {}
    value: "ExtendedProperty"
    properties = get_properties(cls)
    for attr, value in list(properties.items()):
        if attr == "extension_type":
            continue
        properties[attr] = extend_property(value)
        value._s2e_properties.parent_type = model_type
        fields[attr] = pydantic_field(value)
        annotations[attr] = fields[attr][0]
    # print(fields, annotations)
    # Set __annotations__ so that help(), etc. work properly
    if model_type:
        create_model_extras(cls)
    cls.__annotations__ = annotations
    # Create and return the Pydantic model
    model = create_model(cls.__name__, **fields, __base__=BaseModel)
    cls.pydantic_model = model
    model.stix_class = cls
    cls.__doc__ = cls.__doc__ or getattr(cls, "description", None)
    model.__doc__ = cls.__doc__
    cls.schema = model.model_json_schema(mode="validation", schema_generator=Gen)
    if defs := cls.schema.pop("$defs", None):
        cls.schema["$defs"] = defs
    AUTOMODEL_REGISTRY.append(cls)
    return cls


def create_model_extras(cls: Type[ExtendedStixType]):
    if stix2.v21._Observable in cls.mro():
        extension_type = "new-sco"
        cls.base_schema = "https://raw.githubusercontent.com/oasis-open/cti-stix2-json-schemas/master/schemas/common/cyber-observable-core.json"
    elif stix2.v21._DomainObject in cls.mro():
        extension_type = "new-sdo"
        cls.base_schema = "https://github.com/oasis-open/cti-stix2-json-schemas/raw/refs/heads/master/schemas/common/core.json"
    elif stix2.v21._Extension in cls.mro():
        extension_type = cls.extension_type
        cls.with_extension = cls
    else:
        return
    if (
        not hasattr(cls, "extension_definition")
        and not getattr(cls, "with_extension", None)
    ) or stix2.v21._Extension in cls.mro():
        cls.extension_definition = create_extension_definition(cls, extension_type)
    if not getattr(cls, "with_extension", None):
        cls.with_extension = get_extension(cls, extension_type)

    if stix2.v21._Extension in cls.mro():
        pass


def create_extension_definition(
    cls: Type[ExtendedStixType], extension_type
) -> stix2.ExtensionDefinition:
    id = "extension-definition--" + str(uuid.uuid5(namespace, cls._type))
    cls.extension_created = getattr(
        cls, "extension_created", ExtensionType.extension_created
    )
    cls.extension_modified = getattr(cls, "extension_created", cls.extension_created)
    cls.extension_version = getattr(
        cls, "extension_version", ExtensionType.extension_version
    )
    properties = (
        list(filter(lambda x: x != "extension_type", get_properties(cls)))
        if extension_type in ["property-extension", "toplevel-property-extension"]
        else None
    )
    return stix2.ExtensionDefinition(
        id="extension-definition--" + str(uuid.uuid5(namespace, cls._type)),
        created_by_ref=DOGESEC_IDENTITY_REF,
        created=cls.extension_created,
        modified=cls.extension_modified,
        name=getattr(cls, "name", cls.__name__),
        description=getattr(cls, "extension_description", cls.__doc__),
        schema=schema_base + f"{extension_type}/{cls._type}.json",
        version=cls.extension_version or "1.0",
        extension_types=[extension_type],
        object_marking_refs=S2E_MARKING_REFS,
        extension_properties=properties,
    )

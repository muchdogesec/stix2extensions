import contextlib
from datetime import UTC, datetime
from enum import EnumType
import uuid
import stix2
from stix2.properties import Property
import stix2.properties as stixprops
import stix2.utils
from typing import (
    Annotated,
    Literal,
    List,
    Any,
)
from pydantic import (
    Field,
    constr,
    conint,
    confloat,
    StrictStr,
    StrictBool,
    StringConstraints,
)
from pydantic.json_schema import SkipJsonSchema

from .definitions import (
    STIX_ID_RE,
    ExtensionDict,
    _reference_regex_from_valid_types,
)
from .constants import S2E_NAMESPACE


class S2EProperty:
    field_name = ""
    parent_type = ""

    def __init__(
        self,
        property,
        description=None,
        examples=None,
        title=None,
        pydantic_kwargs=None,
    ):
        self.description = description
        self.examples = examples
        self.title = title
        self.property: Property = property
        self.pydantic_kwargs = pydantic_kwargs or {}

    def add_example(self, *examples):
        self.examples = self.examples or []
        self.examples.extend(examples)


class ExtendedProperty(Property):
    _s2e_properties: S2EProperty = None


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
                uuid.uuid5(S2E_NAMESPACE, property._s2e_properties.parent_type + "example")
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
                            S2E_NAMESPACE, property._s2e_properties.parent_type + str(i)
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
        if (
            isinstance(property.type, stixprops.Property)
            or stixprops.Property in property.type.mro()
        ):
            return pydantic_type(property.type)

        from .automodel import automodel
        from stix2.base import _STIXBase

        if hasattr(property.type, "pydantic_model") or _STIXBase in property.type.mro():
            return automodel(property.type).pydantic_model
        return dict  # Fallback for now, actual automodel call needs context

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
                            _t + "--" + str(uuid.uuid5(S2E_NAMESPACE, _t))
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
        stixprops.TimestampProperty: datetime,
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
    kwargs = property._s2e_properties.pydantic_kwargs
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
            if not examples:
                examples.append(transform_examples(default_fn()))
    if getattr(property, "required", None):
        kwargs.pop("default_factory", None)
    if examples:
        kwargs.update(examples=examples)
    return typ, Field(**kwargs)


def extend_property(
    property: "Property|ExtendedProperty",
    description=None,
    examples=None,
    title=None,
    **pydantic_kwargs,
):
    if hasattr(property, "_s2e_properties"):
        return property
    property._s2e_properties = S2EProperty(
        property,
        description=description,
        examples=examples,
        title=title,
        pydantic_kwargs=pydantic_kwargs,
    )
    return property

import uuid
import stix2
from stix2.registry import class_for_type
from stix2.v21.base import _STIXBase, _Extension
import stix2.v21.base as stix2_v21_base
from typing import (
    ClassVar,
    Type,
)
from datetime import datetime
from pydantic import BaseModel
from stix2.properties import Property

from .definitions import (
    get_extension_type_name,
    get_properties,
)
from .constants import (
    S2E_NAMESPACE,
    DOGESEC_IDENTITY_REF,
    CONST_CREATED,
    SCHEMA_BASE,
    S2E_MARKING_REFS,
)


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


def get_extension(cls: Type[ExtendedStixType], _extension_type):
    extension_name = cls.extension_definition["id"]
    NameExtension = class_for_type(cls.extension_definition["id"], "2.1", "extensions")
    if not NameExtension:

        @stix2.CustomExtension(type=extension_name, properties={})
        class NameExtension:
            extension_type = _extension_type

    return NameExtension


def create_model_extras(cls: Type[ExtendedStixType]):
    if stix2_v21_base._Observable in cls.mro():
        extension_type = "new-sco"
        cls.base_schema = "https://raw.githubusercontent.com/oasis-open/cti-stix2-json-schemas/master/schemas/common/cyber-observable-core.json"
    elif stix2_v21_base._DomainObject in cls.mro():
        extension_type = "new-sdo"
        cls.base_schema = "https://github.com/oasis-open/cti-stix2-json-schemas/raw/refs/heads/master/schemas/common/core.json"
    elif stix2_v21_base._Extension in cls.mro():
        extension_type = cls.extension_type
        cls.with_extension = cls
    else:
        return
    if (
        not hasattr(cls, "extension_definition")
        and not getattr(cls, "with_extension", None)
    ) or stix2_v21_base._Extension in cls.mro():
        cls.extension_definition = create_extension_definition(cls, extension_type)
    if not getattr(cls, "with_extension", None):
        cls.with_extension = get_extension(cls, extension_type)


def create_extension_definition(
    cls: Type[ExtendedStixType], extension_type
) -> stix2.ExtensionDefinition:
    id = "extension-definition--" + str(uuid.uuid5(S2E_NAMESPACE, cls._type))
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
        id="extension-definition--" + str(uuid.uuid5(S2E_NAMESPACE, cls._type)),
        created_by_ref=DOGESEC_IDENTITY_REF,
        created=cls.extension_created,
        modified=cls.extension_modified,
        name=getattr(cls, "name", cls.__name__),
        description=getattr(cls, "extension_description", cls.__doc__),
        schema=SCHEMA_BASE + f"{get_extension_type_name(cls)}/{cls._type}.json",
        version=cls.extension_version or "1.0",
        extension_types=[extension_type],
        object_marking_refs=S2E_MARKING_REFS,
        extension_properties=properties,
    )

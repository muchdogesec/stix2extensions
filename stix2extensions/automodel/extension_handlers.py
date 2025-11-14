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
    get_title,
)
from .constants import (
    S2E_NAMESPACE,
    DOGESEC_IDENTITY_REF,
    CONST_CREATED,
    SCHEMA_BASE,
    S2E_MARKING_REFS,
)


class AutomodelExtensionBase(object):
    extension_name: str
    extension_description: str | None
    extension_version: str = "1.0"
    extension_modified: datetime | str = None
    extension_created: datetime | str = CONST_CREATED
    base_schema_ref: str = None


class AutomodelStixType(_STIXBase, AutomodelExtensionBase):
    pydantic_model: BaseModel
    schema: dict
    extension_definition: stix2.ExtensionDefinition
    with_extension: Type["_Extension"]
    _properties: ClassVar[dict[str, Property]]


def get_extension(cls: Type[AutomodelStixType], _extension_type):
    extension_name = cls.extension_definition["id"]
    NameExtension = class_for_type(cls.extension_definition["id"], "2.1", "extensions")
    if not NameExtension:

        @stix2.CustomExtension(type=extension_name, properties={})
        class NameExtension:
            extension_type = _extension_type

    return extension_name, NameExtension


def create_model_extras(cls: Type[AutomodelStixType]):
    if stix2_v21_base._Observable in cls.mro():
        extension_type = "new-sco"
        cls.base_schema_ref = "https://raw.githubusercontent.com/oasis-open/cti-stix2-json-schemas/master/schemas/common/cyber-observable-core.json"
    elif stix2_v21_base._DomainObject in cls.mro():
        extension_type = "new-sdo"
        cls.base_schema_ref = "https://github.com/oasis-open/cti-stix2-json-schemas/raw/refs/heads/master/schemas/common/core.json"
    elif stix2_v21_base._Extension in cls.mro():
        extension_type = cls.extension_type
        cls.extension_klass = cls
        cls.with_extension = cls
    else:
        return
    if (
        not hasattr(cls, "extension_definition")
        and not getattr(cls, "with_extension", None)
    ) or stix2_v21_base._Extension in cls.mro():
        cls.extension_definition = create_extension_definition(cls, extension_type)
    if not getattr(cls, "with_extension", None):
        cls.with_extension, cls.extension_klass = get_extension(cls, extension_type)


def create_extension_definition(
    cls: Type[AutomodelStixType], extension_type
) -> stix2.ExtensionDefinition:
    id = "extension-definition--" + str(uuid.uuid5(S2E_NAMESPACE, cls._type))
    cls.extension_created = getattr(
        cls, "extension_created", AutomodelExtensionBase.extension_created
    )
    cls.extension_modified = getattr(cls, "extension_created", cls.extension_created)
    cls.extension_version = getattr(
        cls, "extension_version", AutomodelExtensionBase.extension_version
    )
    properties = (
        list(filter(lambda x: x != "extension_type", get_properties(cls)))
        if extension_type in ["property-extension", "toplevel-property-extension"]
        else None
    )
    title = get_title(cls)
    if cls._type.startswith('extension-definition--'):
        stix_id = cls._type
    else:
        stix_id = "extension-definition--" + str(uuid.uuid5(S2E_NAMESPACE, cls._type))
    return stix2.ExtensionDefinition(
        id=stix_id,
        created_by_ref=DOGESEC_IDENTITY_REF,
        created=cls.extension_created,
        modified=cls.extension_modified,
        name=getattr(cls, "extension_name", cls.__name__),
        description=getattr(cls, "extension_description", cls.__doc__),
        schema=SCHEMA_BASE + f"{get_extension_type_name(cls)}/{title}.json",
        version=cls.extension_version or "1.0",
        extension_types=[extension_type],
        object_marking_refs=S2E_MARKING_REFS,
        extension_properties=properties,
    )

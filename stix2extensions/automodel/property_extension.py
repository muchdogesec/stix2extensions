import enum
import uuid
from stix2.v21.base import _STIXBase21
from .automodel import namespace
import stix2
from stix2.v21.vocab import EXTENSION_TYPE_PROPERTY_EXTENSION, EXTENSION_TYPE_TOPLEVEL_PROPERTY_EXTENSION

class ExtensionTypes(enum.StrEnum):
    PROPERTY_EXTENSION = EXTENSION_TYPE_PROPERTY_EXTENSION
    TOPLEVEL_PROPERTY_EXTENSION = EXTENSION_TYPE_TOPLEVEL_PROPERTY_EXTENSION


def CustomPropertyExtension(extension_id: str, extension_type: ExtensionTypes, properties):
    initial_type = extension_id
    assert extension_type in ExtensionTypes, "unsupported extension_type"
    if not extension_id.endswith("-ext") and not extension_id.startswith("extension-definition--"):
        extension_id = "extension-definition--" + str(uuid.uuid5(namespace, initial_type))
    def wrapper(cls):
        cls.extension_type = extension_type
        cls.initial_type = initial_type
        new_cls = stix2.CustomExtension(extension_id, properties)(cls)
        return new_cls
    return wrapper

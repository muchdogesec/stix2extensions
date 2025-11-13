from datetime import datetime
import json
from typing import Dict, Literal, Type
import typing
from pydantic import BaseModel
from pydantic_core import core_schema
from typing_extensions import Annotated
from pydantic import RootModel
from pydantic.json_schema import GenerateJsonSchema
from stix2.serialization import serialize as stix_serialize
from stix2.base import _Extension


if typing.TYPE_CHECKING:
    from .automodel import AutomodelStixType


_UUID_RE = r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"
STIX_ID_RE = r"^[a-z][a-z0-9]*(-[a-z0-9]+)*--[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"


def _reference_regex_from_valid_types(valid_types):
    if isinstance(valid_types, str):
        valid_types = [valid_types]
    types_pattern = "|".join(valid_types)
    return rf"^({types_pattern})--{_UUID_RE}$"


def get_extension_type_name(model: Type["AutomodelStixType"]):
    from stix2 import base

    if base._Extension in model.mro():
        dir = "properties"
    elif base._DomainObject in model.mro():
        dir = "sdos"
    elif base._Observable in model.mro():
        dir = "scos"
    else:
        dir = "misc"
    return dir


def get_title(cls: Type["AutomodelStixType"]):
    return getattr(cls, "initial_type", cls._type)


def get_properties(cls: Type["AutomodelStixType"]):
    return getattr(cls, "_toplevel_properties", cls._properties)


class ExtensionDict(Dict[str, Dict]):
    """Dict with fixed keys and pattern-based dynamic keys."""

    PATTERN = _reference_regex_from_valid_types("extension-definition")

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return core_schema.dict_schema(
            keys_schema=core_schema.str_schema(pattern=cls.PATTERN),
            values_schema=core_schema.dict_schema(),
        )

    @classmethod
    def __get_pydantic_json_schema__(cls, schema: core_schema.CoreSchema, handler):
        value_schema = core_schema.dict_schema()
        return {
            "type": "object",
            "patternProperties": {cls.PATTERN: value_schema},
            "additionalProperties": value_schema,
        }


class Gen(GenerateJsonSchema):
    def datetime_schema(self, schema):
        return {
            "$ref": "https://raw.githubusercontent.com/oasis-open/cti-stix2-json-schemas/master/schemas/common/timestamp.json"
        }

    def _update_class_schema(self, json_schema, cls, config):
        if hasattr(cls, "stix_class"):
            stix_cls: Type["AutomodelStixType"] = cls.stix_class
            props = {
                k: v
                for k, v in json_schema.pop("properties").items()
                if k
                not in [
                    "created_by_ref",
                    "created",
                    "modified",
                    "extensions",
                    "object_marking_refs",
                    "granular_markings",
                    "spec_version",
                    "defanged",
                    "external_references",
                ]
            }
            extension_instance = None
            if hasattr(stix_cls, "extension_definition"):
                extension_id = stix_cls.extension_definition["id"]
                extension_instance = stix_cls.extension_klass()
            elif _Extension in stix_cls.mro():
                extension_id = stix_cls._type
                extension_instance = stix_cls()

            if extension_instance:
                props["extensions"] = dict(
                    type="object",
                    additionalProperties=dict(type="object"),
                    properties={
                        extension_id: dict(
                            type="object",
                            const=json.loads(stix_serialize(extension_instance)),
                        ),
                    },
                    required=[extension_id],
                )
                required: list = json_schema.setdefault("required", [])
                required.append("extensions")
            if getattr(stix_cls, "base_schema_ref", None):
                json_schema["allOf"] = [
                    {"$ref": stix_cls.base_schema_ref},
                    dict(properties=props),
                ]
            else:
                json_schema.update(properties=props)
            json_schema["$schema"] = "https://json-schema.org/draft/2020-12/schema"
            if hasattr(stix_cls, "_type"):
                json_schema["title"] = get_title(stix_cls)
        super()._update_class_schema(json_schema, cls, config)
        return json_schema

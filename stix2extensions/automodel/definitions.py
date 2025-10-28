from datetime import datetime
from typing import Dict, Literal
from pydantic import BaseModel
from pydantic_core import core_schema
from typing_extensions import Annotated
from pydantic import RootModel
from pydantic.json_schema import GenerateJsonSchema


_UUID_RE = r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"
STIX_ID_RE = r"^[a-z][a-z0-9]*(-[a-z0-9]+)*--[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"


def _reference_regex_from_valid_types(valid_types):
    if isinstance(valid_types, str):
        valid_types = [valid_types]
    types_pattern = "|".join(valid_types)
    return rf"^({types_pattern})--{_UUID_RE}$"


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


class Timestamp(RootModel):
    root: datetime


class Gen(GenerateJsonSchema):
    def generate_inner(self, schema):
        if schema.get("cls") == Timestamp:
            super().generate_inner(schema)
            return {
                "$ref": "https://raw.githubusercontent.com/oasis-open/cti-stix2-json-schemas/master/schemas/common/timestamp.json"
            }
        json_schema = super().generate_inner(schema)
        return json_schema

    def _update_class_schema(self, json_schema, cls, config):
        if hasattr(cls, "stix_class"):
            base_schema = "https://raw.githubusercontent.com/oasis-open/cti-stix2-json-schemas/master/schemas/common/cyber-observable-core.json"
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
                ]
            }
            json_schema["allOf"] = [
                {"$ref": base_schema},
                dict(properties=props),
            ]
            json_schema["$schema"] = "https://json-schema.org/draft/2020-12/schema"
            if hasattr(cls.stix_class, '_type'):
                json_schema["title"] = cls.stix_class._type
        super()._update_class_schema(json_schema, cls, config)
        return json_schema

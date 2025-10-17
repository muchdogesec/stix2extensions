from typing import Dict, Literal
from pydantic import BaseModel
from pydantic_core import core_schema
from typing_extensions import Annotated


_UUID_RE = r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"


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
            values_schema=core_schema.dict_schema()
        )
    
    @classmethod
    def __get_pydantic_json_schema__(cls, schema: core_schema.CoreSchema, handler):
        value_schema = core_schema.dict_schema()
        return {
            "type": "object",
            "patternProperties": {
                cls.PATTERN: value_schema
            },
            "additionalProperties": value_schema
        }
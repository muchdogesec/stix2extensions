from typing import (
    Any,
    Type,
)
from pydantic import (
    BaseModel,
    create_model,
)

from .definitions import (
    Gen,
    get_properties,
)

from .property_converters import (
    extend_property,
    pydantic_field,
    ExtendedProperty,  # For TYPE_CHECKING
)
from .extension_handlers import (
    AutomodelStixType,
    create_model_extras,
)

AUTOMODEL_REGISTRY: list[Type["AutomodelStixType"]] = []


def automodel(cls: Type[AutomodelStixType]):
    if cls in AUTOMODEL_REGISTRY:
        return cls
    annotations = dict(getattr(cls, "__annotations__", {}))
    model_type = getattr(cls, "_type", None)

    fields: dict[str, tuple[Any, Any]] = {}  # Explicitly type fields
    value: ExtendedProperty  # Use imported ExtendedProperty type hint
    properties = get_properties(cls)
    for attr, value in list(properties.items()):
        if attr == "extension_type":
            continue
        properties[attr] = extend_property(value)
        value._s2e_properties.parent_type = model_type
        fields[attr] = pydantic_field(value)
        annotations[attr] = fields[attr][0]
    # Set __annotations__ so that help(), etc. work properly
    if model_type:
        create_model_extras(cls)
    cls.__annotations__ = annotations
    # Create and return the Pydantic model
    model = create_model(cls.__name__, **fields, __base__=BaseModel)
    cls.pydantic_model = model
    model.stix_class = cls
    cls.__doc__ = cls.__doc__ or getattr(cls, "extension_description", None)
    model.__doc__ = cls.__doc__
    cls.schema = model.model_json_schema(mode="validation", schema_generator=Gen)
    if defs := cls.schema.pop("$defs", None):
        cls.schema["$defs"] = defs
    AUTOMODEL_REGISTRY.append(cls)
    return cls

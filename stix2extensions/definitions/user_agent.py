from stix2 import CustomObservable
from stix2.properties import (
    ExtensionsProperty,
    ReferenceProperty,
    IDProperty,
    ListProperty,
    StringProperty,
    TypeProperty,
)

from stix2extensions.automodel.automodel import auto_model, extend_property
from .._extensions import user_agent_ExtensionDefinitionSMO

_type = "user-agent"


@auto_model
@CustomObservable(
    _type,
    [
        (
            "string",
            extend_property(
                StringProperty(required=True),
                description="Full user-agent string reported by the client",
                examples=[
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
                ],
            ),
        ),
    ],
    id_contrib_props=["string"],
)
class UserAgent(object):
    pass

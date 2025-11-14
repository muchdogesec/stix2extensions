from stix2 import CustomObservable
from stix2.properties import (
    StringProperty,
)

from stix2extensions.automodel import AutomodelExtensionBase, automodel, extend_property

_type = "user-agent"


@automodel
@CustomObservable(
    _type,
    [
        (
            "value",
            extend_property(
                StringProperty(required=True),
                description="Full user-agent string reported by the client",
                examples=[
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
                ],
            ),
        ),
    ],
    id_contrib_props=["value"],
)
class UserAgent(AutomodelExtensionBase):
    extension_description = "This extension creates a new SCO that can be used to represent user agents used in HTTP request. It is designed to be used when the Network Traffic SCO with HTTP request extension cannot be used due to lack of request information needed for the required properties."

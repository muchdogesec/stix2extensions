from stix2 import CustomObservable
from stix2.properties import (
    StringProperty,
)

from stix2extensions.automodel import AutomodelExtensionBase, automodel, extend_property

_type = "phone-number"


@automodel
@CustomObservable(
    _type,
    [
        (
            "value",
            extend_property(
                StringProperty(required=True),
                description="An E.164 formatted phone number.",
                examples=["14155552671", "442071838750"],
            ),
        ),
        (
            "country",
            extend_property(
                StringProperty(),
                description="Three letter ISO (ISO-3166-1 alpha-3) country code the number was issues. Should match intentional dialing prefix in number.",
                examples=["USA", "GBR", "DEU"],
            ),
        ),
        (
            "connection",
            extend_property(
                StringProperty(),
                description="The type of connection the number resolves to.",
                examples=["mobile", "landline", "VoIP"],
            ),
        ),
        (
            "provider",
            extend_property(
                StringProperty(),
                description="Telecommunications provider or carrier of the phone number",
                examples=["Verizon", "AT&T", "Vodafone"],
            ),
        ),
    ],
    id_contrib_props=["value"],
)
class Phonenumber(AutomodelExtensionBase):
    extension_description = (
        "This extension creates a new SCO that can be used to represent phone numbers."
    )

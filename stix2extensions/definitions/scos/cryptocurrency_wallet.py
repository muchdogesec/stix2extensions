from stix2 import CustomObservable
from stix2.properties import (
    ReferenceProperty,
    StringProperty,
)

from stix2extensions.automodel import AutomodelExtensionBase, automodel, extend_property

_type = "cryptocurrency-wallet"


@automodel
@CustomObservable(
    _type,
    [
        (
            "value",
            extend_property(
                StringProperty(required=True),
                description="Cryptocurrency wallet address or identifier",
                examples=["bc1qw508d6qejxtdg4y5r3zarvary0c5xw7kygt080"],
            ),
        ),
        (
            "holder_ref",
            extend_property(
                ReferenceProperty(valid_types="identity", spec_version="2.1"),
                description="Defines the STIX ID of an identity object of the owner. If it is a custodial wallet this could be an exhange, or otherwise a known person/organisation.",
                examples=["identity--1ee9d44a-c962-59b5-adbf-e47cb3f03b92"],
            ),
        ),
    ],
    id_contrib_props=["value"],
)
class CryptocurrencyWallet(AutomodelExtensionBase):
    extension_description = "This extension creates a new SCO that can be used to represent cryptocurrency wallets."

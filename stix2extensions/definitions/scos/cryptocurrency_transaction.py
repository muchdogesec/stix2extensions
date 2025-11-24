from typing import OrderedDict
from stix2 import CustomObservable
from stix2.properties import (
    ListProperty,
    StringProperty,
    TimestampProperty,
    FloatProperty,
    ReferenceProperty,
    EmbeddedObjectProperty,
)

from stix2extensions.automodel import AutomodelExtensionBase, extend_property, automodel
from stix2.v21.base import _STIXBase21


_type = "cryptocurrency-transaction"

@automodel
class AddressAndAmount(_STIXBase21):
    _properties = OrderedDict([
        ("amount", FloatProperty(min=0)),
        ("address_ref", ReferenceProperty(valid_types="cryptocurrency-wallet")),
    ])


@automodel
@CustomObservable(
    _type,
    [
        (
            "symbol",
            extend_property(
                StringProperty(required=True),
                description="3 digit code for the cryptocurrency.",
                examples=["BTC", "ETH"],
            ),
        ),
        (
            "value",
            extend_property(
                StringProperty(required=True),
                description="The transaction hash.",
                examples=["0.0125"],
            ),
        ),
        (
            "fee",
            extend_property(
                FloatProperty(min=0.0),
                description="The transaction fee.",
                examples=[0.00000728, 0.1],
            ),
        ),
        (
            "execution_time",
            extend_property(
                TimestampProperty(),
                description="Timestamp when the transaction was executed",
                examples=["2024-06-15T12:45:30Z"],
            ),
        ),
        (
            "input",
            extend_property(
                ListProperty(EmbeddedObjectProperty(type=AddressAndAmount)),
                description="Input addresses and amounts for the transaction",
            ),
        ),
        (
            "output",
            extend_property(
                ListProperty(EmbeddedObjectProperty(type=AddressAndAmount)),
                description="Output addresses and amounts for the transaction",
            ),
        ),
    ],
    id_contrib_props=["value", "symbol"],
)
class CryptocurrencyTransaction(AutomodelExtensionBase):
    extension_description = "This extension creates a new SCO that can be used to represent cryptocurrency transactions."

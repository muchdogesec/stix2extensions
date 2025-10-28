from stix2 import CustomObservable
from stix2.properties import (
    ListProperty,
    StringProperty,
    TimestampProperty,
    DictionaryProperty,
    FloatProperty,
)

from stix2extensions.automodel.automodel import extend_property, auto_model


_type = "cryptocurrency-transaction"


@auto_model
@CustomObservable(
    "cryptocurrency-transaction",
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
                ListProperty(DictionaryProperty()),
                description="Input addresses and amounts for the transaction",
            ),
        ),
        (
            "output",
            extend_property(
                ListProperty(DictionaryProperty()),
                description="Output addresses and amounts for the transaction",
            ),
        ),
    ],
    id_contrib_props=["value", "symbol"],
)
class CryptocurrencyTransaction(object):
    pass

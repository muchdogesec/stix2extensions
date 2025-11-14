from stix2 import CustomObservable
from stix2.properties import (
    ReferenceProperty,
    StringProperty,
    BooleanProperty,
    TimestampProperty,
    EnumProperty,
)

from stix2extensions.automodel import AutomodelExtensionBase, automodel, extend_property

_type = "payment-card"


@automodel
@CustomObservable(
    _type,
    [
        (
            "format",
            extend_property(
                EnumProperty(allowed=["credit", "debit", "prepaid"]),
                description="The type of card.",
            ),
        ),
        (
            "value",
            extend_property(
                StringProperty(required=True),
                description="Full card number.",
                examples=["4111111111111111", "4242424242424242"],
            ),
        ),
        (
            "scheme",
            extend_property(
                StringProperty(),
                description="Card scheme or network",
                examples=["VISA", "MASTERCARD", "AMEX"],
            ),
        ),
        (
            "brand",
            extend_property(
                StringProperty(),
                description="Card brand or product name",
                examples=["VISA", "MASTERCARD", "AMEX"],
            ),
        ),
        (
            "currency",
            extend_property(
                StringProperty(),
                description="3 letter ISO (ISO 4217) currency code for currency card is denominated in.",
                examples=["USD", "EUR", "GBP"],
            ),
        ),
        (
            "issuer_ref",
            extend_property(
                ReferenceProperty(valid_types="identity", spec_version="2.1"),
                description="STIX Identity reference to the issuing financial institution",
                examples=["identity--9bef1584-289b-41fe-81b4-a5d72b7746d6"],
            ),
        ),
        (
            "holder_ref",
            extend_property(
                ReferenceProperty(valid_types="identity", spec_version="2.1"),
                description="STIX identity eference to the cardholder identity",
                examples=["identity--9fcd0db9-8115-4e33-ae00-674806395cf1"],
            ),
        ),
        (
            "start_date",
            extend_property(
                TimestampProperty(),
                description="The valid from date on the card in datetime format.",
                examples=["2023-01-01T00:00:00Z"],
            ),
        ),
        (
            "expiration_date",
            extend_property(
                TimestampProperty(),
                description="The expiration on the card in datetime format.e",
                examples=["2026-12-31T23:59:59Z"],
            ),
        ),
        (
            "security_code",
            extend_property(
                StringProperty(),
                description="Card security code (CVV/CVC) where applicable",
                examples=["123", "1234"],
            ),
        ),
        (
            "level",
            extend_property(
                StringProperty(),
                description="Card level describes the issuers classification. For example, classic level often refers to a basic or introductory level card with no monthly fees.",
                examples=["CLASSIC"],
            ),
        ),
        (
            "is_commercial",
            extend_property(
                BooleanProperty(),
                description="If the card is registered for commercial use (vs. personal use).",
            ),
        ),
        (
            "is_prepaid",
            extend_property(
                BooleanProperty(),
                description="If the card is prepaid",
            ),
        ),
    ],
    id_contrib_props=["value"],
)
class PaymentCard(AutomodelExtensionBase):
    extension_description = "This extension creates a new SCO that can be used to represent different types of payment card."

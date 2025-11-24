from stix2 import CustomObservable
from stix2.properties import (
    ReferenceProperty,
    StringProperty,
)

from stix2extensions.automodel import extend_property, automodel


_type = "bank-account"


@automodel
@CustomObservable(
    _type,
    [
        (
            "country_ref",
            extend_property(
                ReferenceProperty(valid_types="location"),
                description="STIX reference to the Location of the account.",
                examples=["location--4e9a8b79-6776-56e3-b72c-cb19a086b6a8", "location--14c8eade-a3b5-5ec3-8850-b3c82d4cee38"],
            ),
        ),
        (
            "currency",
            extend_property(
                StringProperty(),
                description="3 letter ISO (ISO 4217) currency code for currency of account.",
                examples=["USD", "EUR", "SAR", "NGN"],
            ),
        ),
        (
            "issuer_ref",
            extend_property(
                ReferenceProperty(valid_types="identity", spec_version="2.1"),
                description="STIX reference to the entity that issued the account (typically a bank)",
                examples=["identity--9bef1584-289b-41fe-81b4-a5d72b7746d6"],
            ),
        ),
        (
            "holder_ref",
            extend_property(
                ReferenceProperty(valid_types="identity", spec_version="2.1"),
                description="STIX reference to the account holder identity",
                examples=["dentity--9fcd0db9-8115-4e33-ae00-674806395cf1"],
            ),
        ),
        (
            "account_number",
            extend_property(
                StringProperty(),
                description="The account number assigned by the bank to the customer",
                examples=["1234567890", "987654321"],
            ),
        ),
        (
            "iban",
            extend_property(
                StringProperty(),
                description="Full IBAN number of the account.",
                examples=["GB29 NWBK 6016 1331 9268 19", "DE89 3704 0044 0532 0130 00"],
            ),
        ),
        (
            "bic",
            extend_property(
                StringProperty(),
                description="Full BIC (aka SWIFT) code of the account.",
                examples=["DEUTDEFF", "NWBKGB2L"],
            ),
        ),
    ],
    id_contrib_props=["iban", "account_number"],
)
class BankAccount(object):
    extension_description = "This extension creates a new SCO that can be used to represent bank account details."
    at_least_one_of = ["iban", "account_number"]

    def _check_object_constraints(self):
        self._check_at_least_one_property(self.at_least_one_of)

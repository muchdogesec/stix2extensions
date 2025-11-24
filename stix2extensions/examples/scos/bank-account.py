import uuid
from uuid import UUID

from stix2extensions.definitions.scos import BankAccount

namespace = UUID("00abedb4-aa42-466c-9c01-fed23315a9b7")

example_bankAccountSCO = BankAccount(
    id="bank-account--" + str(uuid.uuid5(namespace, f"GB33BUKB20201555555555")),
    issuer_ref="identity--" + str(uuid.uuid5(namespace, f"Big Bank")),
    country_ref="location--d9a1d93a-9141-4afe-9f67-95c357287f73",
    currency="GBP",
    holder_ref="identity--fb76b7b8-8701-5d8b-a143-0283847f6638",
    iban="GB33BUKB20201555555555",
    bic="DEMOGB22XXX",
)

examples = [
    example_bankAccountSCO,
]

import uuid
from uuid import UUID

from stix2extensions.definitions.scos import Phonenumber

namespace = UUID("00abedb4-aa42-466c-9c01-fed23315a9b7")

example_PhoneNumberSCO = Phonenumber(
    id="phone-number--" + str(uuid.uuid5(namespace, f"07890129093")),
    value="4407890129093",
    country="GBR",
    connection="mobile",
    provider="Big Network",
)

examples = [
    example_PhoneNumberSCO,
]
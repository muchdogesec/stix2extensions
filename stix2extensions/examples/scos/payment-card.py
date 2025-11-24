import uuid
from uuid import UUID

from stix2extensions.definitions.scos import PaymentCard

namespace = UUID("00abedb4-aa42-466c-9c01-fed23315a9b7")

example_paymentCardSCO = PaymentCard(
    id="payment-card--" + str(uuid.uuid5(namespace, f"4242424242424242")),
    format="credit",
    value="4242424242424242",
    scheme="VISA",
    brand="VISA",
    currency="GBP",
    issuer_ref="identity--9bef1584-289b-41fe-81b4-a5d72b7746d6",
    holder_ref="identity--9fcd0db9-8115-4e33-ae00-674806395cf1",
    start_date="1999-01-01T00:00:00Z",
    expiration_date="2000-01-02T23:59:59Z",
    security_code="999",
    level="CLASSIC",
    is_commercial=False,
    is_prepaid=False,
)

examples = [
    example_paymentCardSCO,
]
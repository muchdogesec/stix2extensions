import uuid
from uuid import UUID

from stix2extensions.definitions.scos import CryptocurrencyTransaction

namespace = UUID("00abedb4-aa42-466c-9c01-fed23315a9b7")

example_CryptocurrencyTransactionSCO = CryptocurrencyTransaction(
    id="cryptocurrency-transaction--"
    + str(uuid.uuid5(namespace, f"3FZbgi29cpjq2GjdwV8eyHuJJnkLtktZc5")),
    symbol="BTC",
    value="3FZbgi29cpjq2GjdwV8eyHuJJnkLtktZc5",
    fee="0.00000728",
    execution_time="2022-10-02T15:22:21Z",
    input=[
        {
            "address_ref": "cryptocurrency-wallet--b1bc02bd-f10d-40e4-86d1-9e2ef3aa919f",
            "amount": 0.84,
        }
    ],
    output=[
        {
            "address_ref": "cryptocurrency-wallet--b6ae6083-875f-5fe9-84b9-89e168f89406",
            "amount": 0.8,
        },
        {
            "address_ref": "cryptocurrency-wallet--4d18102a-f35a-4176-9509-f96a3370d067",
            "amount": 0.04,
        },
    ],
)

examples = [
    example_CryptocurrencyTransactionSCO,
]

import uuid
from uuid import UUID

from stix2extensions.definitions.scos import CryptocurrencyWallet

namespace = UUID("00abedb4-aa42-466c-9c01-fed23315a9b7")

example_CryptocurrencyWalletSCO = CryptocurrencyWallet(
    id="cryptocurrency-wallet--" + str(uuid.uuid5(namespace, f"1KFHE7w8BhaENAswwryaoccDb6qcT6DbYY")),
    value="1KFHE7w8BhaENAswwryaoccDb6qcT6DbYY",
    holder_ref="identity--1ee9d44a-c962-59b5-adbf-e47cb3f03b92",
)

examples = [
    example_CryptocurrencyWalletSCO,
]
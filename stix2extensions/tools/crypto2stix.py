from dataclasses import dataclass
from datetime import datetime
from itertools import chain
from typing import Union
import uuid
import requests
from ..cryptocurrency_transaction import CryptocurrencyTransaction
from ..cryptocurrency_wallet import CryptocurrencyWallet
from .._extensions import (
    cryptocurrency_transaction_ExtensionDefinitionSMO,
    cryptocurrency_wallet_ExtensionDefinitionSMO,
)

WALLET_NAMESPACE_UUID = uuid.UUID("00abedb4-aa42-466c-9c01-fed23315a9b7")

@dataclass
class TxnData:
    block_id: str = ""
    execution_time: str = ""
    fee: str = ""
    inputs: list[tuple[str, str]] = ()
    outputs: list[tuple[str, str]] = ()
    hash: str = ""

@dataclass
class WalletData:
    address: str = ""
    transactions: list[str] = ()


class Crypto2Stix:
    symbol = None
    processed_wallets = set()

    def get_transaction_object(self, hash) -> CryptocurrencyTransaction:
        raise NotImplementedError("should be implemented in subclass")

    def get_transaction_data(self, tx_hash) -> TxnData:
        raise NotImplementedError("should be implemented in subclass")

    def get_wallet_data(self, addr) -> WalletData:
        raise NotImplementedError("should be implemented in subclass")

    def create_transaction_object(self, tx_data: TxnData):
        transaction_object = CryptocurrencyTransaction(
            type="cryptocurrency-transaction",
            spec_version="2.1",
            symbol=self.symbol,
            hash=tx_data.hash,
            block_id=tx_data.block_id,
            fee=tx_data.fee,
            execution_time=tx_data.execution_time,
            input=[
                {
                    "address_ref": f"cryptocurrency-wallet--{str(uuid.uuid5(WALLET_NAMESPACE_UUID, addr))}",
                    "amount": amount,
                }
                for addr, amount in tx_data.inputs
            ],
            output=[
                {
                    "address_ref": f"cryptocurrency-wallet--{str(uuid.uuid5(WALLET_NAMESPACE_UUID, addr))}",
                    "amount": amount,
                }
                for addr, amount in tx_data.outputs
            ],
            extensions={
                cryptocurrency_transaction_ExtensionDefinitionSMO.id: {
                    "extension_type": "new-sco"
                }
            },
        )
        return transaction_object

    def create_wallet_object(self, addr):
        # wallet = self.get_wallet_data(addr)
        return CryptocurrencyWallet(
            type="cryptocurrency-wallet",
            spec_version="2.1",
            id=self.get_wallet_id(addr),
            address=addr,
            extensions={
                cryptocurrency_wallet_ExtensionDefinitionSMO.id: {
                    "extension_type": "new-sco"
                }
            },
        )

    @staticmethod
    def get_wallet_id(wallet_addr):
        return f"cryptocurrency-wallet--{str(uuid.uuid5(WALLET_NAMESPACE_UUID, wallet_addr))}"

    @staticmethod
    def get_txn_id(txn_hash):
        return f"cryptocurrency-transaction--{str(uuid.uuid5(WALLET_NAMESPACE_UUID, txn_hash))}"
    
    def process_transaction(self, txn: Union[str, TxnData]):
        tx_data = self.get_transaction_data(txn)
        objects = [self.create_transaction_object(tx_data)]
        for addr, _ in chain(tx_data.inputs, tx_data.outputs):
            if addr in self.processed_wallets:
                continue
            objects.append(
                self.create_wallet_object(addr)
            )
            self.processed_wallets.add(addr)
        return objects
    
    def process_wallet(self, addr: str, transactions_only=True, wallet_only=False):
        objects = []
        wallet = WalletData(address=addr)
        if not wallet_only:
            wallet = self.get_wallet_data(addr)
        objects.append(self.create_wallet_object(wallet.address))
        self.processed_wallets.add(addr)
        for txn_hash in wallet.transactions:
            if transactions_only:
                txn = self.get_transaction_data(txn_hash)
                objects.append(self.create_transaction_object(txn))
            else:
                objects.extend(self.process_transaction(txn_hash))
        return objects
            


class BTC2Stix(Crypto2Stix):
    symbol = "BTC"

    def get_transaction_object(self, hash):
        return super().get_transaction_object(hash)

    def get_transaction_data(self, txn):
        if isinstance(txn, str):
            url = f"https://blockchain.info/rawtx/{txn}"
            response = requests.get(url)
            tx_data = response.json()
        else:
            tx_data = txn

        inputs = [
            (inp["prev_out"]["addr"], inp["prev_out"]["value"] / 100000000)
            for inp in tx_data["inputs"]
            if "addr" in inp["prev_out"]
        ]
        outputs = [
            (out["addr"], out["value"] / 100000000)
            for out in tx_data["out"]
            if "addr" in out
        ]
        block_id = str(tx_data["block_height"])
        execution_time = datetime.utcfromtimestamp(tx_data["time"]).isoformat() + "Z"
        return TxnData(
            block_id=block_id,
            execution_time=execution_time,
            fee=str(tx_data["fee"] / 100000000),
            inputs=inputs,
            outputs=outputs,
            hash=txn,
        )

    def get_wallet_data(self, wallet_address):
        url = f"https://blockchain.info/rawaddr/{wallet_address}"
        response = requests.get(url)
        wallet_data = response.json()
        return WalletData(address=wallet_address, transactions=wallet_data["txs"])
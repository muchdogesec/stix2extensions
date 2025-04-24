from dataclasses import dataclass
from datetime import UTC, datetime
from itertools import chain
import time
from typing import Union
import uuid
import requests
from ..cryptocurrency_transaction import CryptocurrencyTransaction
from ..cryptocurrency_wallet import CryptocurrencyWallet
from .._extensions import (
    cryptocurrency_transaction_ExtensionDefinitionSMO,
    cryptocurrency_wallet_ExtensionDefinitionSMO,
)

# this is the oasis uuid
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
            # block_id=tx_data.block_id,
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
    DIVIDER = 100000000

    def get_transaction_object(self, hash):
        url = f"https://btcscan.org/api/tx/{hash}"
        return self.make_request(url)

    def get_transaction_data(self, txn):
        if isinstance(txn, str):
            txn = self.get_transaction_object(txn)
        if isinstance(txn, TxnData):
            return txn

        inputs = []
        for inp in txn.get("vin", []):
            prevout = self.parse_tx_address_and_value(inp.get("prevout", {}))
            if prevout:
                inputs.append(prevout)

        outputs = []
        for out in txn.get("vout", []):
            out_parsed = self.parse_tx_address_and_value(out)
            if out_parsed:
                outputs.append(out_parsed)

        status = txn.get("status", {})
        block_id = str(status.get("block_height")) if status.get("block_height") else None
        block_time = status.get("block_time")
        execution_time = datetime.fromtimestamp(block_time, tz=UTC) if block_time else None

        return TxnData(
            block_id=block_id,
            execution_time=execution_time,
            fee=str(txn["fee"] / self.DIVIDER) if txn.get("fee") else "0",
            inputs=inputs,
            outputs=outputs,
            hash=txn.get("txid"),
        )
    

    def get_wallet_data(self, wallet_address):
        return WalletData(address=wallet_address, transactions=self.get_transactions_by_address(wallet_address))
    
    def get_transactions_by_address(self, address):
        all_txns = []
        last_seen_txid = None

        while True:
            url = f"https://btcscan.org/api/address/{address}/txs/chain"
            if last_seen_txid:
                url += f"/{last_seen_txid}"
            batch = self.make_request(url)
            if not batch:
                break  # No more transactions
            all_txns.extend(batch)
            last_seen_txid = batch[-1]["txid"]
        return all_txns
    
    @classmethod
    def parse_tx_address_and_value(cls, out: dict):
        if not out:
            return
        addr = out.get("scriptpubkey_address")
        value = out.get("value")
        if addr and value is not None:
            return (addr, value / cls.DIVIDER)
        
    def make_request(self, url):
        time.sleep(1)
        for attempt in range(5):
            response = requests.get(url)
            if response.status_code == 429:
                time.sleep(60)
                continue
            response.raise_for_status()
            return response.json()

        raise Exception("Failed to fetch transaction data after 10 retries due to rate limits.")

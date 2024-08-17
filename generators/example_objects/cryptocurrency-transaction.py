import uuid
import stix2
import os
import shutil

from uuid import UUID
from stix2extensions.cryptocurrency_transaction import CryptocurrencyTransaction
# create the directories

tmp_directories = [
    "tmp_object_store",
]

for directory in tmp_directories:
    if not os.path.exists(directory):
        os.makedirs(directory)

# define UUID for generating UUIDv5s -- this is the OASIS namespace for SCOs https://github.com/oasis-open/cti-python-stix2/blob/master/stix2/base.py#L29

namespace=UUID("00abedb4-aa42-466c-9c01-fed23315a9b7")

# Create CryptocurrencyTransaction SCO

example_CryptocurrencyTransactionSCO = CryptocurrencyTransaction(
                    id="cryptocurrency-transaction--"+ str(uuid.uuid5(namespace, f"3FZbgi29cpjq2GjdwV8eyHuJJnkLtktZc5")), # cryptocurrency-transaction--da6911a9-7f49-5d20-ae4e-f9154d1b9a39
                    symbol="BTC",
                    hash="3FZbgi29cpjq2GjdwV8eyHuJJnkLtktZc5",
                    fee="0.00000728",
                    execution_time="2022-10-02T15:22:21Z",
                    input=[
                        {
                            "address_ref": "cryptocurrency-wallet--b1bc02bd-f10d-40e4-86d1-9e2ef3aa919f",
                            "amount": 0.84000000
                        }
                    ],
                    output=[
                        {
                            "address_ref": "cryptocurrency-wallet--b6ae6083-875f-5fe9-84b9-89e168f89406",
                            "amount": 0.80000000
                        },
                        {
                            "address_ref": "cryptocurrency-wallet--4d18102a-f35a-4176-9509-f96a3370d067",
                            "amount": 0.04000000
                        }
                    ],
                    )

# Write the objects to the filestore
## https://stix2.readthedocs.io/en/latest/guide/filesystem.html#FileSystemSource

### Creating FileSystemStore and adding MarkingDefinitionSMO for each directory

fs_directories = {
    "tmp_object_store": example_CryptocurrencyTransactionSCO
}

for directory, cryptocurrency_transaction_sco in fs_directories.items():
    fs_store = stix2.FileSystemStore(directory)
    fs_store.add([cryptocurrency_transaction_sco])

# Now move those files into the standardised locations for easy download

final_directories = [
    "example_objects/scos"
]

for directory in final_directories:
    if not os.path.exists(directory):
        os.makedirs(directory)

shutil.move("tmp_object_store/cryptocurrency-transaction/cryptocurrency-transaction--" + str(uuid.uuid5(namespace, f"3FZbgi29cpjq2GjdwV8eyHuJJnkLtktZc5")) + ".json", "example_objects/scos/cryptocurrency-transaction--" + str(uuid.uuid5(namespace, f"3FZbgi29cpjq2GjdwV8eyHuJJnkLtktZc5")) + ".json")

shutil.rmtree("tmp_object_store")
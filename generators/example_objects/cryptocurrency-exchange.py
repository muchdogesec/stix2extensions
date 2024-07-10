import uuid
import stix2
import os
import shutil

from uuid import UUID
from stix2extensions.cryptocurrency_exchange import CryptocurrencyExchange
# create the directories

tmp_directories = [
    "tmp_object_store",
]

for directory in tmp_directories:
    if not os.path.exists(directory):
        os.makedirs(directory)

# define UUID for generating UUIDv5s -- this is the OASIS namespace for SCOs https://github.com/oasis-open/cti-python-stix2/blob/master/stix2/base.py#L29

namespace=UUID("00abedb4-aa42-466c-9c01-fed23315a9b7")

# Create CryptocurrencyExchange SCO

example_CryptocurrencyExchangeSCO = CryptocurrencyExchange(
                    id="cryptocurrency-exchange--"+ str(uuid.uuid5(namespace, f"coinbase.com")), # cryptocurrency-exchange--1ee9d44a-c962-59b5-adbf-e47cb3f03b92
                    name="Coinbase",
                    domain="coinbase.com",
                    )

# Write the objects to the filestore
## https://stix2.readthedocs.io/en/latest/guide/filesystem.html#FileSystemSource

### Creating FileSystemStore and adding MarkingDefinitionSMO for each directory

fs_directories = {
    "tmp_object_store": example_CryptocurrencyExchangeSCO
}

for directory, cryptocurrency_exchange_sco in fs_directories.items():
    fs_store = stix2.FileSystemStore(directory)
    fs_store.add([cryptocurrency_exchange_sco])

# Now move those files into the standardised locations for easy download

final_directories = [
    "example_objects/scos"
]

for directory in final_directories:
    if not os.path.exists(directory):
        os.makedirs(directory)

shutil.move("tmp_object_store/cryptocurrency-exchange/cryptocurrency-exchange--" + str(uuid.uuid5(namespace, f"coinbase.com")) + ".json", "example_objects/scos/cryptocurrency-exchange--" + str(uuid.uuid5(namespace, f"coinbase.com")) + ".json")

shutil.rmtree("tmp_object_store")
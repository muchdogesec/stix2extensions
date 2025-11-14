import os
import shutil
import uuid
from uuid import UUID

import stix2
from stix2extensions.bank_account import BankAccount

# create the directories

tmp_directories = [
    "tmp_object_store",
]

for directory in tmp_directories:
    if not os.path.exists(directory):
        os.makedirs(directory)

# define UUID for generating UUIDv5s -- this is the OASIS namespace for SCOs https://github.com/oasis-open/cti-python-stix2/blob/master/stix2/base.py#L29

namespace=UUID("00abedb4-aa42-466c-9c01-fed23315a9b7")

# Create bank account SCO

example_bankAccountSCO = BankAccount(
                    id="bank-account--"+ str(uuid.uuid5(namespace, f"GB33BUKB20201555555555")), # bank-account--fb76b7b8-8701-5d8b-a143-0283847f6638
                    bank="Big Bank",
                    country_ref="location--d9a1d93a-9141-4afe-9f67-95c357287f73",
                    currency="GBP",
                    holder_ref="identity--fb76b7b8-8701-5d8b-a143-0283847f6638",
                    iban="GB33BUKB20201555555555",
                    bic="DEMOGB22XXX",
                    )

# Write the objects to the filestore
## https://stix2.readthedocs.io/en/latest/guide/filesystem.html#FileSystemSource

### Creating FileSystemStore and adding MarkingDefinitionSMO for each directory

fs_directories = {
    "tmp_object_store": example_bankAccountSCO
}

for directory, bankaccount_sco in fs_directories.items():
    fs_store = stix2.FileSystemStore(directory)
    fs_store.add([bankaccount_sco])

# Now move those files into the standardised locations for easy download

final_directories = [
    "example_objects/scos"
]

for directory in final_directories:
    if not os.path.exists(directory):
        os.makedirs(directory)

shutil.move("tmp_object_store/bank-account/bank-account--" + str(uuid.uuid5(namespace, f"GB33BUKB20201555555555")) + ".json", "example_objects/scos/bank-account--" + str(uuid.uuid5(namespace, f"GB33BUKB20201555555555")) + ".json")

shutil.rmtree("tmp_object_store")

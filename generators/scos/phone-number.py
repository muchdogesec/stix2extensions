import uuid
import stix2
import os
import shutil

from uuid import UUID

from stix2extensions.phone_number import Phonenumber
# create the directories

tmp_directories = [
    "tmp_object_store",
]

for directory in tmp_directories:
    if not os.path.exists(directory):
        os.makedirs(directory)

# define UUID for generating UUIDv5s -- this is the OASIS namespace for SCOs https://github.com/oasis-open/cti-python-stix2/blob/master/stix2/base.py#L29

namespace=UUID("00abedb4-aa42-466c-9c01-fed23315a9b7")

# Create PhoneNumber SCO

example_PhoneNumberSCO = Phonenumber(
                    id="phone-number--"+ str(uuid.uuid5(namespace, f"07890129093")),
                    number="4407890129093",
                    country="GBR",
                    connection="Mobile",
                    provider="Big Network"
                    )

# Write the objects to the filestore
## https://stix2.readthedocs.io/en/latest/guide/filesystem.html#FileSystemSource

### Creating FileSystemStore and adding MarkingDefinitionSMO for each directory

fs_directories = {
    "tmp_object_store": example_PhoneNumberSCO
}

for directory, phone_number_sco in fs_directories.items():
    fs_store = stix2.FileSystemStore(directory)
    fs_store.add([phone_number_sco])

# Now move those files into the standardised locations for easy download

final_directories = [
    "example_objects/scos"
]

for directory in final_directories:
    if not os.path.exists(directory):
        os.makedirs(directory)

shutil.move("tmp_object_store/phone-number/phone-number--" + str(uuid.uuid5(namespace, f"07890129093")) + ".json", "example_objects/scos/phone-number--" + str(uuid.uuid5(namespace, f"07890129093")) + ".json")

shutil.rmtree("tmp_object_store")
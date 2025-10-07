import uuid
import stix2
import os
import shutil

from uuid import UUID

from stix2extensions.data_source import DataSource
# create the directories

tmp_directories = [
    "tmp_object_store",
]

for directory in tmp_directories:
    if not os.path.exists(directory):
        os.makedirs(directory)

# define UUID for generating UUIDv5s -- this is the OASIS namespace for SCOs https://github.com/oasis-open/cti-python-stix2/blob/master/stix2/base.py#L29

namespace=UUID("00abedb4-aa42-466c-9c01-fed23315a9b7")

# Create DataSource SCO

example_DataSourceSCO = DataSource(
                    id="data-source--"+ str(uuid.uuid5(namespace, f"Powershell Script")),
                    product="windows",
                    category="ps_script",
                    definition="Script Block Logging must be enabled",
                    )

# Write the objects to the filestore
## https://stix2.readthedocs.io/en/latest/guide/filesystem.html#FileSystemSource

### Creating FileSystemStore and adding MarkingDefinitionSMO for each directory

fs_directories = {
    "tmp_object_store": example_DataSourceSCO
}

for directory, data_source_sco in fs_directories.items():
    fs_store = stix2.FileSystemStore(directory)
    fs_store.add([data_source_sco])

# Now move those files into the standardised locations for easy download

final_directories = [
    "example_objects/scos"
]

for directory in final_directories:
    if not os.path.exists(directory):
        os.makedirs(directory)

shutil.move("tmp_object_store/data-source/data-source--" + str(uuid.uuid5(namespace, f"Powershell Script")) + ".json", "example_objects/scos/data-source--" + str(uuid.uuid5(namespace, f"Powershell Script")) + ".json")

shutil.rmtree("tmp_object_store")
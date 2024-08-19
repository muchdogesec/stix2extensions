import uuid
import stix2
import os
import shutil

from uuid import UUID

from stix2extensions.weakness import Weakness
# create the directories

tmp_directories = [
    "tmp_object_store",
]

for directory in tmp_directories:
    if not os.path.exists(directory):
        os.makedirs(directory)

# define UUID for generating UUIDv5s -- use stix2extensions namespace as this is an SDO

namespace=UUID("1abb62b9-e513-5f55-8e73-8f6d7b55c237")

# define values that are recycled between objects

### dogesec-demo

created_by_ref="identity--" + str(uuid.uuid5(namespace, f"dogesec-demo"))
created="2020-01-01T00:00:00.000Z"
modified="2020-01-01T00:00:00.000Z"

# Create Weakness SDO object

### weakness--519a9c84-3c54-5698-bd9a-99bd01f003d1

example_WeaknessSDO = Weakness(
                        id="weakness--"+ str(uuid.uuid5(namespace, f"A demo weakness")),
                        created_by_ref=created_by_ref,
                        created=created,
                        modified=modified,
                        name="CWE Demo",
                        description="A demo weakness",
                        modes_of_introduction=[
                            "Implementation"
                        ],
                        likelihood_of_exploit=[
                            "Medium"
                        ],
                        common_consequences=[
                            "Confidentiality",
                            "Integrity"
                        ],
                        detection_methods=[
                            "Automated Static Analysis"
                        ],
                        external_references=[
                            {
                                "source_name": "cwe",
                                "url": "http://cwe.mitre.org/data/definitions/117.html",
                                "external_id": "CWE-117"
                            }
                        ],
                        object_marking_refs=[
                            "marking-definition--94868c89-83c2-464b-929b-a1a8aa3c8487", # this is TLP:CLEAR
                            "marking-definition--" + str(uuid.uuid5(namespace, f"stix2extensions")) # marking-definition--97ba4e8b-04f6-57e8-8f6e-3a0f0a7dc0fb
                        ]
                    )

# Write the objects to the filestore
## https://stix2.readthedocs.io/en/latest/guide/filesystem.html#FileSystemSource

### Creating FileSystemStore and adding MarkingDefinitionSMO for each directory

fs_directories = {
    "tmp_object_store": example_WeaknessSDO
}

for directory, weakness_sdo in fs_directories.items():
    fs_store = stix2.FileSystemStore(directory)
    fs_store.add([weakness_sdo])

# Now move those files into the standardised locations for easy download

final_directories = [
    "example_objects/sdos"
]

for directory in final_directories:
    if not os.path.exists(directory):
        os.makedirs(directory)

shutil.move("tmp_object_store/weakness/weakness--" + str(uuid.uuid5(namespace, f"A demo weakness")) + "/20200101000000000.json", "example_objects/sdos/weakness--" + str(uuid.uuid5(namespace, f"A demo weakness")) + ".json")

shutil.rmtree("tmp_object_store")
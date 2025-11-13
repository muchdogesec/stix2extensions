import uuid
import stix2
import os
import shutil

from uuid import UUID

from stix2 import Identity
from stix2extensions._extensions import identity_opencti_ExtensionDefinitionSMO
# create the directories

tmp_directories = [
    "tmp_object_store",
]

for directory in tmp_directories:
    if not os.path.exists(directory):
        os.makedirs(directory)

# define UUID for generating UUIDv5s -- use stix2extensions namespace as this is an SDO

namespace=UUID("1abb62b9-e513-5f55-8e73-8f6d7b55c237")

# Create Identity SDO object

### identity--400e3858-6042-592c-83b5-5aac8bcaf24e

example_IdentitySDO = Identity(
                        id="identity--"+ str(uuid.uuid5(namespace, f"example_IdentitySDO")),
                        created_by_ref="identity--c4781245-66e6-57cb-afa3-434232edcc8b",
                        created="2020-01-01T00:00:00.000Z",
                        modified="2020-01-01T00:00:00.000Z",
                        name="Agriculture and agribusiness",
                        description="Private entities specialized in the growth, culture, transport and transformation of plants or livestock for food.",
                        identity_class= "class",
                        x_opencti_aliases = [
                            "Agriculture",
                            "Agribusiness",
                            "Food Production",
                            "Nutritional Supplements"
                        ],
                        object_marking_refs=[
                            "marking-definition--94868c89-83c2-464b-929b-a1a8aa3c8487", # this is TLP:CLEAR
                            "marking-definition--" + str(uuid.uuid5(namespace, f"stix2extensions")) # marking-definition--97ba4e8b-04f6-57e8-8f6e-3a0f0a7dc0fb
                        ],
                        extensions={
							identity_opencti_ExtensionDefinitionSMO.id: {
								"extension_type": "toplevel-property-extension",
							}
						}
                    )

# Write the objects to the filestore
## https://stix2.readthedocs.io/en/latest/guide/filesystem.html#FileSystemSource

### Creating FileSystemStore and adding MarkingDefinitionSMO for each directory

fs_directories = {
    "tmp_object_store": example_IdentitySDO
}

for directory, identity_sdo in fs_directories.items():
    fs_store = stix2.FileSystemStore(directory)
    fs_store.add([identity_sdo])

# Now move those files into the standardised locations for easy download

final_directories = [
    "example_objects/sdos"
]

for directory in final_directories:
    if not os.path.exists(directory):
        os.makedirs(directory)

shutil.move("tmp_object_store/identity/identity--" + str(uuid.uuid5(namespace, f"example_IdentitySDO")) + "/20200101000000000.json", "example_objects/properties/identity--" + str(uuid.uuid5(namespace, f"example_IdentitySDO")) + ".json")

shutil.rmtree("tmp_object_store")
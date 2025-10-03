import uuid
import stix2
import os
import shutil

from uuid import UUID

from stix2 import Location
from stix2extensions._extensions import location_opencti_ExtensionDefinitionSMO

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

# Create Location SDO object

### location--c06ee555-6c92-5d41-9e55-8abb490cb7c1

example_opencti_LocationSDO = Location(
                        id="location--"+ str(uuid.uuid5(namespace, f"A Demo Location")),
                        created_by_ref=created_by_ref,
                        created=created,
                        modified=modified,
                        name="Egypt",
                        country="EG",
                        x_opencti_aliases=[
                            "EGY",
                            "EG"
                        ],
                        x_opencti_location_type=[
                            "Country"
                        ],
                        latitude=26.820553,
                        longitude=30.802498,
                        region="northern-africa",
                        external_references=[
                            {
                              "source_name": "location2stix",
                              "external_id": "EG"
                            },
                            {
                              "source_name": "type",
                              "external_id": "country"
                            },
                            {
                              "source_name": "alpha-2",
                              "external_id": "EG"
                            },
                            {
                              "source_name": "alpha-3",
                              "external_id": "EGY"
                            },
                            {
                              "source_name": "iso_3166-2",
                              "external_id": "ISO 3166-2:EG"
                            },
                            {
                              "source_name": "country-code",
                              "external_id": "818"
                            }                        
                        ],
                        object_marking_refs=[
                            "marking-definition--94868c89-83c2-464b-929b-a1a8aa3c8487", # this is TLP:CLEAR
                            "marking-definition--" + str(uuid.uuid5(namespace, f"stix2extensions")) # marking-definition--97ba4e8b-04f6-57e8-8f6e-3a0f0a7dc0fb
                        ],
                        extensions={
                            location_opencti_ExtensionDefinitionSMO.id: {
                                    "extension_type": "toplevel-property-extension"
                            }
                        }
                    )

# Write the objects to the filestore
## https://stix2.readthedocs.io/en/latest/guide/filesystem.html#FileSystemSource

### Creating FileSystemStore and adding MarkingDefinitionSMO for each directory

fs_directories = {
    "tmp_object_store": example_opencti_LocationSDO
}

for directory, location_sdo in fs_directories.items():
    fs_store = stix2.FileSystemStore(directory)
    fs_store.add([location_sdo])

# Now move those files into the standardised locations for easy download

final_directories = [
    "example_objects/sdos"
]

for directory in final_directories:
    if not os.path.exists(directory):
        os.makedirs(directory)

shutil.move("tmp_object_store/location/location--" + str(uuid.uuid5(namespace, f"A Demo Location")) + "/20200101000000000.json", "example_objects/properties/location--" + str(uuid.uuid5(namespace, f"A Demo Location")) + ".json")

shutil.rmtree("tmp_object_store")
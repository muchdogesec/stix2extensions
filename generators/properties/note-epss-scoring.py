import uuid
import stix2
import os
import shutil

from uuid import UUID

from stix2 import Note
from stix2extensions._extensions import note_epss_scoring_ExtensionDefinitionSMO

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

# Create NoteSDO object

### note--8d62e369-463f-59d7-825b-09185aed39dc

example_NoteSDO = Note(
                        id="note--"+ str(uuid.uuid5(namespace, f"A demo EPSS Note")),
                        created_by_ref=created_by_ref,
                        created=created,
                        modified=modified,
                        content="EPSS Score for CVE-XXX-XXXX",
                        object_refs=[
                            "vulnerability--20b0177f-7b3c-527c-b88c-fca16a0ebf5d"
                        ],
                        object_marking_refs=[
                            "marking-definition--94868c89-83c2-464b-929b-a1a8aa3c8487", # this is TLP:CLEAR
                            "marking-definition--" + str(uuid.uuid5(namespace, f"stix2extensions")) # marking-definition--97ba4e8b-04f6-57e8-8f6e-3a0f0a7dc0fb
                        ],
                        x_epss={
                            "date": "2024-08-18",
                            "score": "0.000750000",
                            "percentile": "0.328570000"
                        },
                        extensions={
                            note_epss_scoring_ExtensionDefinitionSMO.id: {
                                    "extension_type": "toplevel-property-extension"
                            }
                        }
                    )

# Write the objects to the filestore
## https://stix2.readthedocs.io/en/latest/guide/filesystem.html#FileSystemSource

### Creating FileSystemStore and adding MarkingDefinitionSMO for each directory

fs_directories = {
    "tmp_object_store": example_NoteSDO
}

for directory, note_sdo in fs_directories.items():
    fs_store = stix2.FileSystemStore(directory)
    fs_store.add([note_sdo])

# Now move those files into the standardised locations for easy download

final_directories = [
    "example_objects/sdos"
]

for directory in final_directories:
    if not os.path.exists(directory):
        os.makedirs(directory)

shutil.move("tmp_object_store/note/note--" + str(uuid.uuid5(namespace, f"A demo EPSS Note")) + "/20200101000000000.json", "example_objects/properties/note--" + str(uuid.uuid5(namespace, f"A demo EPSS Note")) + ".json")

shutil.rmtree("tmp_object_store")
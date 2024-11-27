import uuid
import stix2
import os
import shutil

from uuid import UUID

from stix2 import Software
from stix2extensions._extensions import software_cpe_properties_ExtensionDefinitionSMO

# create the directories

tmp_directories = [
    "tmp_object_store",
]

for directory in tmp_directories:
    if not os.path.exists(directory):
        os.makedirs(directory)

# Create SoftwareSCO object

### software--fda5adb5-23e5-5089-a256-36f298ba241f"

example_SoftwareSCO = Software(
                        id="software--fda5adb5-23e5-5089-a256-36f298ba241f",
                        name="EGroupware 14.1.20140710 Community Edition",
                        cpe="cpe:2.3:a:egroupware:egroupware:14.1.20140710:*:*:*:community:*:*:*",
                        swid="A1F2EAFC-0523-4257-A9EA-94462CA2BDB8",
                        languages=[
                            "en"
                        ],
                        vendor="egroupware",
                        version="14.1.20140710",
                        x_cpe_struct={
                            "cpe_version": "2.3",
                            "part": "a",
                            "vendor": "egroupware",
                            "product": "egroupware",
                            "version": "14.1.20140710",
                            "update": "*",
                            "edition": "*",
                            "language": "*",
                            "sw_edition": "community",
                            "target_sw": "*",
                            "target_hw": "*",
                            "other": "*"
                        },
                        extensions={
                            software_cpe_properties_ExtensionDefinitionSMO.id: {
                                    "extension_type": "toplevel-property-extension"
                            }
                        }
                    )


# Write the objects to the filestore
## https://stix2.readthedocs.io/en/latest/guide/filesystem.html#FileSystemSource

### Creating FileSystemStore and adding MarkingDefinitionSMO for each directory

fs_directories = {
    "tmp_object_store": example_SoftwareSCO
}

for directory, note_sdo in fs_directories.items():
    fs_store = stix2.FileSystemStore(directory)
    fs_store.add([note_sdo])

# Now move those files into the standardised locations for easy download

final_directories = [
    "example_objects/scos"
]

for directory in final_directories:
    if not os.path.exists(directory):
        os.makedirs(directory)

shutil.move("tmp_object_store/software/software--fda5adb5-23e5-5089-a256-36f298ba241f.json", "example_objects/properties/software--fda5adb5-23e5-5089-a256-36f298ba241f.json")

shutil.rmtree("tmp_object_store")
import uuid
import stix2
import os
import shutil

from uuid import UUID

from stix2 import Indicator
from stix2extensions._extensions import indicator_vulnerable_cpes_ExtensionDefinitionSMO
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

# Create Indicator SDO object

### indicator--f23c4675-951d-5490-8203-f0e568c1feb8

example_IndicatorSDO = Indicator(
                        id="indicator--"+ str(uuid.uuid5(namespace, f"A demo Indicator")),
                        created_by_ref=created_by_ref,
                        created=created,
                        modified=modified,
                        valid_from=modified,
                        name="CVE-XXX-XXXX",
                        pattern="([(software:cpe='cpe:2.3:a:dell:powerscale_onefs:9.1.0:*:*:*:*:*:*:*' AND software:cpe='cpe:2.3:h:eq-3:homematic_ccu2:-:*:*:*:*:*:*:*')])",
                        pattern_type="stix",
                        external_references=[
                            {
                                "source_name": "cve",
                                "url": "https://nvd.nist.gov/vuln/detail/CVE-XXX-XXXX",
                                "external_id": "CVE-XXX-XXXX"
                            }
                        ],
                        object_marking_refs=[
                            "marking-definition--94868c89-83c2-464b-929b-a1a8aa3c8487", # this is TLP:CLEAR
                            "marking-definition--" + str(uuid.uuid5(namespace, f"stix2extensions")) # marking-definition--97ba4e8b-04f6-57e8-8f6e-3a0f0a7dc0fb
                        ],
                        x_cpes= {
                            "vulnerable": [
                                {
                                    "criteria": "cpe:2.3:a:dell:powerscale_onefs:9.0.0:*:*:*:*:*:*:*",
                                    "matchCriteriaId": "30687628-5C7F-4BB5-B990-93703294FDF0"
                                }
                            ],
                            "not_vulnerable": [
                                {
                                    "criteria": "cpe:2.3:a:dell:powerscale_onefs:9.1.0:*:*:*:*:*:*:*",
                                    "matchCriteriaId": "68291D44-DBE1-4923-A848-04E64288DC23"
                                }
                            ]
                        },
                        extensions={
							indicator_vulnerable_cpes_ExtensionDefinitionSMO.id: {
								"extension_type": "toplevel-property-extension",
							}
						}
                    )

# Write the objects to the filestore
## https://stix2.readthedocs.io/en/latest/guide/filesystem.html#FileSystemSource

### Creating FileSystemStore and adding MarkingDefinitionSMO for each directory

fs_directories = {
    "tmp_object_store": example_IndicatorSDO
}

for directory, indicator_sdo in fs_directories.items():
    fs_store = stix2.FileSystemStore(directory)
    fs_store.add([indicator_sdo])

# Now move those files into the standardised locations for easy download

final_directories = [
    "example_objects/sdos"
]

for directory in final_directories:
    if not os.path.exists(directory):
        os.makedirs(directory)

shutil.move("tmp_object_store/indicator/indicator--" + str(uuid.uuid5(namespace, f"A demo Indicator")) + "/20200101000000000.json", "example_objects/properties/indicator--" + str(uuid.uuid5(namespace, f"A demo Indicator")) + ".json")

shutil.rmtree("tmp_object_store")
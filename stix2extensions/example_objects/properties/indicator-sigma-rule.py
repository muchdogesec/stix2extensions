import uuid
import stix2
import os
import shutil

from uuid import UUID

from stix2 import Indicator
from stix2extensions._extensions import indicator_sigma_rule_ExtensionDefinitionSMO
# create the directories

tmp_directories = [
    "tmp_object_store",
]

for directory in tmp_directories:
    if not os.path.exists(directory):
        os.makedirs(directory)

# define UUID for generating UUIDv5s -- use stix2extensions namespace as this is an SDO

namespace=UUID("1abb62b9-e513-5f55-8e73-8f6d7b55c237")

# Create Indicator SDO object

### indicator--330e2030-1dc2-45e6-be13-9342b102621b

example_IndicatorSDO = Indicator(
                        id="indicator--330e2030-1dc2-45e6-be13-9342b102621b",
                        created_by_ref="identity--c4781245-66e6-57cb-afa3-434232edcc8b",
                        created="2021-09-12T00:00:00.000Z",
                        modified="2022-10-09T00:00:00.000Z",
                        valid_from="2021-09-12T00:00:00.000Z",
                        name="Okta Policy Modified or Deleted",
                        description="Detects when an Okta policy is modified or deleted.",
                        pattern="id: 6a4c842a-986f-43f0-8f3f-d98cdd36e01e\ntitle: Okta Policy Modified or Deleted\ndescription: Detects when an Okta policy is modified or deleted.\nlevel: medium\nstatus: stable\ndetection:\n    selection:\n        eventtype:\n        - policy.lifecycle.update\n        - policy.lifecycle.delete\n    condition: selection\nlogsource:\n    product: okta\n    service: okta\nfalsepositives:\n- Okta Policies being modified or deleted may be performed by a system administrator.\n- Verify whether the user identity, user agent, and/or hostname should be making changes\n    in your environment.\n- Okta Policies modified or deleted from unfamiliar users should be investigated.\n    If known behavior is causing false positives, it can be exempted from the rule.\ntags:\n- attack.t1547\n- attack.command_and_control\n- cve.2024-56520\n- tlp.clear\nrelated:\n-   id: 1667a172-ed4c-463c-9969-efd92195319a\n    type: renamed\nauthor: identity--c4781245-66e6-57cb-afa3-434232edcc8b\nreferences:\n- https://developer.okta.com/docs/reference/api/system-log/\n- https://developer.okta.com/docs/reference/api/event-types/\ndate: 2021-09-12\nmodified: 2022-10-09\n",
                        pattern_type="sigma",
                        x_sigma_type="base",
                        x_sigma_level="medium",
                        x_sigma_status="stable",
                        object_marking_refs=[
                            "marking-definition--94868c89-83c2-464b-929b-a1a8aa3c8487", # this is TLP:CLEAR
                            "marking-definition--" + str(uuid.uuid5(namespace, f"stix2extensions")) # marking-definition--97ba4e8b-04f6-57e8-8f6e-3a0f0a7dc0fb
                        ],
                        extensions={
							indicator_sigma_rule_ExtensionDefinitionSMO.id: {
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

shutil.move("tmp_object_store/indicator/indicator--330e2030-1dc2-45e6-be13-9342b102621b" + "/20221009000000000.json", "example_objects/properties/indicator--330e2030-1dc2-45e6-be13-9342b102621b" + ".json")

shutil.rmtree("tmp_object_store")
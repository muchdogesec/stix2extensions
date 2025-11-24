import uuid
from uuid import UUID

from stix2extensions.definitions.sdos import Weakness

namespace = UUID("1abb62b9-e513-5f55-8e73-8f6d7b55c237")

created_by_ref = "identity--" + str(uuid.uuid5(namespace, f"dogesec-demo"))
created = "2020-01-01T00:00:00.000Z"
modified = "2020-01-01T00:00:00.000Z"

example_WeaknessSDO = Weakness(
    id="weakness--" + str(uuid.uuid5(namespace, f"A demo weakness")),
    created_by_ref=created_by_ref,
    created=created,
    modified=modified,
    name="CWE Demo",
    description="A demo weakness",
    modes_of_introduction=["Implementation"],
    likelihood_of_exploit="Medium",
    common_consequences=["Confidentiality", "Integrity"],
    detection_methods=["Automated Static Analysis"],
    external_references=[
        {"source_name": "cwe", "url": "http://cwe.mitre.org/data/definitions/117.html", "external_id": "CWE-117"}
    ],
    object_marking_refs=[
        "marking-definition--94868c89-83c2-464b-929b-a1a8aa3c8487",
        "marking-definition--" + str(uuid.uuid5(namespace, f"stix2extensions")),
    ],
)

examples = [
    example_WeaknessSDO,
]
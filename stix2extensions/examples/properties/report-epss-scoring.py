import uuid
from uuid import UUID

from stix2 import Report
from stix2extensions.definitions.properties import (
    ReportEPSSScoring,
)

report_epss_scoring_ExtensionDefinitionSMO = ReportEPSSScoring.extension_definition

# define UUID for generating UUIDv5s -- use stix2extensions namespace as this is an SDO
namespace = UUID("1abb62b9-e513-5f55-8e73-8f6d7b55c237")

# define values that are recycled between objects
created_by_ref = "identity--" + str(uuid.uuid5(namespace, f"dogesec-demo"))
created = "2020-01-01T00:00:00.000Z"
modified = "2020-01-01T00:00:00.000Z"

# Create Report SDO object

example_ReportSDO = Report(
    id="report--" + str(uuid.uuid5(namespace, f"example_ReportSDO")),
    created_by_ref=created_by_ref,
    created=created,
    modified=modified,
    published=created,
    name="EPSS Scores: CVE-XXX-XXXX",
    object_refs=["vulnerability--20b0177f-7b3c-527c-b88c-fca16a0ebf5d"],
    object_marking_refs=[
        "marking-definition--94868c89-83c2-464b-929b-a1a8aa3c8487",
        "marking-definition--" + str(uuid.uuid5(namespace, f"stix2extensions")),
    ],
    x_epss=[
        {"date": "2024-08-19", "score": "0.000900000", "percentile": "0.428920000"},
        {"date": "2024-08-18", "score": "0.000750000", "percentile": "0.328570000"},
    ],
    extensions={
        report_epss_scoring_ExtensionDefinitionSMO.id: {
            "extension_type": "toplevel-property-extension"
        }
    },
)

examples = [
    example_ReportSDO,
]

from datetime import UTC, datetime, timezone
import uuid
import stix2
import os
import shutil
import json

from stix2 import Bundle
from stix2.base import STIXJSONEncoder
from stix2 import ExtensionDefinition
from stix2 import FileSystemStore
from uuid import UUID

from stix2extensions.definitions.phone_number import Phonenumber
from stix2extensions import definitions

# define UUID for generating UUIDv5s

namespace = UUID("1abb62b9-e513-5f55-8e73-8f6d7b55c237")

# define values that are recycled between objects

### dogesec

DOGESEC_IDENTITY_REF = "identity--" + str(uuid.uuid5(namespace, f"dogesec"))
created = "2020-01-01T00:00:00.000Z"
modified = "2020-01-01T00:00:00.000Z"
schema_base = (
    "https://raw.githubusercontent.com/muchdogesec/stix2extensions/main/schemas/"
)

### mitre TLP:CLEAR and stix4doge

S2E_MARKING_REFS = [
    "marking-definition--94868c89-83c2-464b-929b-a1a8aa3c8487",  # this is TLP:CLEAR
    "marking-definition--" + str(uuid.uuid5(namespace, f"stix2extensions")),  #
]

# ### Location OpenCTI Extension SMO

location_opencti_ExtensionDefinitionSMO = ExtensionDefinition(
    id="extension-definition--"
    + str(
        uuid.uuid5(namespace, f"location-opencti")
    ),  # extension-definition--b9c1f945-80be-519d-9d7f-0cede26032e9
    created_by_ref=DOGESEC_IDENTITY_REF,
    created=created,
    modified=modified,
    name="Location SDO OpenCTI Properties",
    description="This extension adds OpenCTI-specific properties to STIX Location SDOs.",
    schema=schema_base + "properties/location-opencti.json",
    version="1.0",
    extension_types=["toplevel-property-extension"],
    extension_properties=["x_opencti_aliases", "x_opencti_location_type"],
    object_marking_refs=S2E_MARKING_REFS,
)

### Indicator Vulnerable CPEs Extension SMO

indicator_vulnerable_cpes_ExtensionDefinitionSMO = ExtensionDefinition(
    id="extension-definition--"
    + str(
        uuid.uuid5(namespace, f"indicator-vulnerable-cpes")
    ),  # extension-definition--ad995824-2901-5f6e-890b-561130a239d4
    created_by_ref=DOGESEC_IDENTITY_REF,
    created=created,
    modified=datetime(2020, 1, 1, tzinfo=UTC),
    name="Indicator SDO Vulnerable CPEs Properties",
    description="This extension adds new properties to Indicator SDOs to list CPE vulnerable inside a pattern.",
    schema=schema_base + "properties/indicator-vulnerable-cpes.json",
    version="1.0",
    extension_types=["toplevel-property-extension"],
    extension_properties=["x_cpes"],
    object_marking_refs=S2E_MARKING_REFS,
)

### Report EPSS Scoring SMO

report_epss_scoring_ExtensionDefinitionSMO = ExtensionDefinition(
    id="extension-definition--"
    + str(
        uuid.uuid5(namespace, f"report-epss-scoring")
    ),  # extension-definition--f80cce10-5ac0-58d1-9e7e-b4ed0cc4dbb9
    created_by_ref=DOGESEC_IDENTITY_REF,
    created=created,
    modified=datetime(2020, 1, 1, tzinfo=UTC),
    name="Report SDO EPSS Scoring Properties",
    description="This extension adds new properties to Report SDOs to capture EPSS scores for CVEs.",
    schema=schema_base + "properties/report-epss-scoring.json",
    version="1.0",
    extension_types=["toplevel-property-extension"],
    extension_properties=["x_epss"],
    object_marking_refs=S2E_MARKING_REFS,
)

### Software CPE SMO

software_cpe_properties_ExtensionDefinitionSMO = ExtensionDefinition(
    id="extension-definition--"
    + str(
        uuid.uuid5(namespace, f"software-cpe-properties")
    ),  # extension-definition--82cad0bb-0906-5885-95cc-cafe5ee0a500
    created_by_ref=DOGESEC_IDENTITY_REF,
    created=created,
    modified=datetime(2025, 10, 3, tzinfo=UTC),
    name="Software SCO CPE Properties",
    description="This extension adds new properties to Software SCOs to capture CPE data.",
    schema=schema_base + "properties/software-cpe-properties.json",
    version="1.0",
    extension_types=["toplevel-property-extension"],
    extension_properties=["x_cpe_struct", "x_revoked", "x_created", "x_modified"],
    object_marking_refs=S2E_MARKING_REFS,
)

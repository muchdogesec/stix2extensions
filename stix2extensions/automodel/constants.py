import uuid
from datetime import UTC, datetime

S2E_NAMESPACE = uuid.UUID("1abb62b9-e513-5f55-8e73-8f6d7b55c237")

### dogesec

DOGESEC_IDENTITY_REF = "identity--" + str(uuid.uuid5(S2E_NAMESPACE, f"dogesec"))
CONST_CREATED = datetime(2020, 1, 1, tzinfo=UTC)
SCHEMA_BASE = (
    "https://raw.githubusercontent.com/muchdogesec/stix2extensions/main/automodel_generated/schemas/"
)

### mitre TLP:CLEAR and stix4doge

S2E_MARKING_REFS = [
    "marking-definition--94868c89-83c2-464b-929b-a1a8aa3c8487",  # this is TLP:CLEAR
    "marking-definition--" + str(uuid.uuid5(S2E_NAMESPACE, f"stix2extensions")),  #
]
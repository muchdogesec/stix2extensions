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

namespace=UUID("1abb62b9-e513-5f55-8e73-8f6d7b55c237")

# define values that are recycled between objects

### dogesec

DOGESEC_IDENTITY_REF="identity--" + str(uuid.uuid5(namespace, f"dogesec"))
created="2020-01-01T00:00:00.000Z"
modified="2020-01-01T00:00:00.000Z"
schema_base="https://raw.githubusercontent.com/muchdogesec/stix2extensions/main/schemas/"

### mitre TLP:CLEAR and stix4doge

S2E_MARKING_REFS=[
    "marking-definition--94868c89-83c2-464b-929b-a1a8aa3c8487", # this is TLP:CLEAR
    "marking-definition--" + str(uuid.uuid5(namespace, f"stix2extensions")) # 
]

# Create New Extension Defintion SMO
## https://stix2.readthedocs.io/en/latest/api/v21/stix2.v21.common.html

### Phone number SMO

phone_number_ExtensionDefinitionSMO = Phonenumber.extension_definition

### Cryptocurrency Transaction SMO

cryptocurrency_transaction_ExtensionDefinitionSMO = definitions.CryptocurrencyTransaction.extension_definition

### Data Source SMO

data_source_ExtensionDefinitionSMO = definitions.DataSource.extension_definition

### Weakness SMO

weakness_ExtensionDefinitionSMO = definitions.Weakness.extension_definition

### Exploit SMO

exploit_ExtensionDefinitionSMO = definitions.Exploit.extension_definition

### Payment Card SMO

payment_card_ExtensionDefinitionSMO = definitions.PaymentCard.extension_definition

### User Agent SMO

user_agent_ExtensionDefinitionSMO = definitions.UserAgent.extension_definition

### Cryptocurrency Wallet SMO

cryptocurrency_wallet_ExtensionDefinitionSMO = definitions.CryptocurrencyWallet.extension_definition

### Bank Account SMO

bank_account_ExtensionDefinitionSMO = definitions.BankAccount.extension_definition

### Vulnerability Scoring Extension SMO

vulnerability_scoring_ExtensionDefinitionSMO = ExtensionDefinition(
                        id="extension-definition--" + str(uuid.uuid5(namespace, f"vulnerability-scoring")), # extension-definition--2c5c13af-ee92-5246-9ba7-0b958f8cd34a
                        created_by_ref=DOGESEC_IDENTITY_REF,
                        created=created,
                        modified=datetime(2025, 10, 3, 0, 0, tzinfo=UTC),
                        name="Vulnerability SDO Scoring Properties",
                        description="This extension adds new properties to Vulnerbility SDOs to provide scoring.",
                        schema=schema_base+"properties/vulnerability-scoring.json",
                        version="1.0",
                        extension_types=[
                            "toplevel-property-extension"
                        ],
                        extension_properties=[
                            "x_cvss",
                        ],
                        object_marking_refs=S2E_MARKING_REFS
                    )

### Vulnerability OpenCTI Extension SMO

vulnerability_opencti_ExtensionDefinitionSMO = ExtensionDefinition(
                        id="extension-definition--" + str(uuid.uuid5(namespace, f"vulnerability-opencti")), # xtension-definition--ec658473-1319-53b4-879f-488e47805554
                        created_by_ref=DOGESEC_IDENTITY_REF,
                        created=created,
                        modified=modified,
                        name="Vulnerability SDO OpenCTI Properties",
                        description="This extension adds OpenCTI-specific properties to STIX Vulnerability SDOs, including CVSS v2/v3/v4 metrics, CWE, CISA KEV, and EPSS.",
                        schema=schema_base+"properties/vulnerability-opencti.json",
                        version="1.0",
                        extension_types=[
                            "toplevel-property-extension"
                        ],
                        extension_properties=[
                            "x_opencti_cvss_v2_base_score",
                            "x_opencti_cvss_v2_temporal_score",
                            "x_opencti_cvss_v2_vector_string",
                            "x_opencti_cvss_v2_access_vector",
                            "x_opencti_cvss_v2_access_complexity",
                            "x_opencti_cvss_v2_authentication",
                            "x_opencti_cvss_v2_confidentiality_impact",
                            "x_opencti_cvss_v2_integrity_impact",
                            "x_opencti_cvss_v2_availability_impact",
                            "x_opencti_cvss_v2_exploitability",
                            "x_opencti_cvss_v2_remediation_level",
                            "x_opencti_cvss_v2_report_confidence",
                            "x_opencti_cvss_base_score",
                            "x_opencti_cvss_temporal_score",
                            "x_opencti_cvss_vector_string",
                            "x_opencti_cvss_base_severity",
                            "x_opencti_cvss_attack_vector",
                            "x_opencti_cvss_attack_complexity",
                            "x_opencti_cvss_privileges_required",
                            "x_opencti_cvss_user_interaction",
                            "x_opencti_cvss_scope",
                            "x_opencti_cvss_confidentiality_impact",
                            "x_opencti_cvss_integrity_impact",
                            "x_opencti_cvss_availability_impact",
                            "x_opencti_cvss_exploit_code_maturity",
                            "x_opencti_cvss_remediation_level",
                            "x_opencti_cvss_report_confidence",
                            "x_opencti_cvss_v4_base_score",
                            "x_opencti_cvss_v4_vector_string",
                            "x_opencti_cvss_v4_base_severity",
                            "x_opencti_cvss_v4_attack_vector",
                            "x_opencti_cvss_v4_attack_complexity",
                            "x_opencti_cvss_v4_attack_requirements",
                            "x_opencti_cvss_v4_privileges_required",
                            "x_opencti_cvss_v4_user_interaction",
                            "x_opencti_cvss_v4_confidentiality_impact_v",
                            "x_opencti_cvss_v4_confidentiality_impact_s",
                            "x_opencti_cvss_v4_integrity_impact_v",
                            "x_opencti_cvss_v4_integrity_impact_s",
                            "x_opencti_cvss_v4_availability_impact_v",
                            "x_opencti_cvss_v4_availability_impact_s",
                            "x_opencti_cvss_v4_exploit_maturity",
                            "x_opencti_cwe",
                            "x_opencti_cisa_kev",
                            "x_opencti_epss_score",
                            "x_opencti_epss_percentile"
                        ],
                        object_marking_refs=S2E_MARKING_REFS
                    )

### Location OpenCTI Extension SMO

location_opencti_ExtensionDefinitionSMO = ExtensionDefinition(
                        id="extension-definition--" + str(uuid.uuid5(namespace, f"location-opencti")), # extension-definition--b9c1f945-80be-519d-9d7f-0cede26032e9
                        created_by_ref=DOGESEC_IDENTITY_REF,
                        created=created,
                        modified=modified,
                        name="Location SDO OpenCTI Properties",
                        description="This extension adds OpenCTI-specific properties to STIX Location SDOs.",
                        schema=schema_base+"properties/location-opencti.json",
                        version="1.0",
                        extension_types=[
                            "toplevel-property-extension"
                        ],
                        extension_properties=[
                            "x_opencti_aliases",
                            "x_opencti_location_type"
                        ],
                        object_marking_refs=S2E_MARKING_REFS
                    )

### Indicator Vulnerable CPEs Extension SMO

indicator_vulnerable_cpes_ExtensionDefinitionSMO = ExtensionDefinition(
                        id="extension-definition--" + str(uuid.uuid5(namespace, f"indicator-vulnerable-cpes")), # extension-definition--ad995824-2901-5f6e-890b-561130a239d4
                        created_by_ref=DOGESEC_IDENTITY_REF,
                        created=created,
                        modified=datetime(2020, 1, 1, tzinfo=UTC),
                        name="Indicator SDO Vulnerable CPEs Properties",
                        description="This extension adds new properties to Indicator SDOs to list CPE vulnerable inside a pattern.",
                        schema=schema_base+"properties/indicator-vulnerable-cpes.json",
                        version="1.0",
                        extension_types=[
                            "toplevel-property-extension"
                        ],
                        extension_properties=[
                            "x_cpes"
                        ],
                        object_marking_refs=S2E_MARKING_REFS
                    )

### Report EPSS Scoring SMO

report_epss_scoring_ExtensionDefinitionSMO = ExtensionDefinition(
                        id="extension-definition--" + str(uuid.uuid5(namespace, f"report-epss-scoring")), # extension-definition--f80cce10-5ac0-58d1-9e7e-b4ed0cc4dbb9
                        created_by_ref=DOGESEC_IDENTITY_REF,
                        created=created,
                        modified=datetime(2020, 1, 1, tzinfo=UTC),
                        name="Report SDO EPSS Scoring Properties",
                        description="This extension adds new properties to Report SDOs to capture EPSS scores for CVEs.",
                        schema=schema_base+"properties/report-epss-scoring.json",
                        version="1.0",
                        extension_types=[
                            "toplevel-property-extension"
                        ],
                        extension_properties=[
                            "x_epss"
                        ],
                        object_marking_refs=S2E_MARKING_REFS
                    )

### Software CPE SMO

software_cpe_properties_ExtensionDefinitionSMO = ExtensionDefinition(
                        id="extension-definition--" + str(uuid.uuid5(namespace, f"software-cpe-properties")), # extension-definition--82cad0bb-0906-5885-95cc-cafe5ee0a500
                        created_by_ref=DOGESEC_IDENTITY_REF,
                        created=created,
                        modified=datetime(2025, 10, 3, tzinfo=UTC),
                        name="Software SCO CPE Properties",
                        description="This extension adds new properties to Software SCOs to capture CPE data.",
                        schema=schema_base+"properties/software-cpe-properties.json",
                        version="1.0",
                        extension_types=[
                            "toplevel-property-extension"
                        ],
                        extension_properties=[
                            "x_cpe_struct",
                            "x_revoked",
                            "x_created",
                            "x_modified"
                        ],
                        object_marking_refs=S2E_MARKING_REFS
                    )

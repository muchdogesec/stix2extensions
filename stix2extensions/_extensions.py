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

phone_number_ExtensionDefinitionSMO = ExtensionDefinition(
                        id="extension-definition--" + str(uuid.uuid5(namespace, f"phone-number")), # extension-definition--14a97ee2-e666-5ada-a6bd-b7177f79e211
                        created_by_ref=DOGESEC_IDENTITY_REF,
                        created=created,
                        modified=datetime(2020, 1, 1, tzinfo=UTC),
                        name="Phone Number",
                        description="This extension creates a new SCO that can be used to represent phone numbers.",
                        schema=schema_base+"scos/phone-number.json",
                        version="1.0",
                        extension_types=[
                            "new-sco"
                        ],
                        object_marking_refs=S2E_MARKING_REFS
                    )

### Cryptocurrency Transaction SMO

cryptocurrency_transaction_ExtensionDefinitionSMO = ExtensionDefinition(
                        id="extension-definition--" + str(uuid.uuid5(namespace, f"cryptocurrency-transaction")), # extension-definition--151d042d-4dcf-5e44-843f-1024440318e5
                        created_by_ref=DOGESEC_IDENTITY_REF,
                        created=created,
                        modified=datetime(2020, 1, 1, tzinfo=UTC),
                        name="Cryptocurrency Transaction",
                        description="This extension creates a new SCO that can be used to represent cryptocurrency transactions.",
                        schema=schema_base+"scos/cryptocurrency-transaction.json",
                        version="1.0",
                        extension_types=[
                            "new-sco"
                        ],
                        object_marking_refs=S2E_MARKING_REFS
                    )

### Data Source SMO

data_source_ExtensionDefinitionSMO = ExtensionDefinition(
                        id="extension-definition--" + str(uuid.uuid5(namespace, f"data-source")), # extension-definition--afeeb724-bce2-575e-af3d-d705842ea84b
                        created_by_ref=DOGESEC_IDENTITY_REF,
                        created=created,
                        modified=modified,
                        name="Data Source",
                        description="This extension creates a new SCO that can be used to represent data sources. Very similar to x-mitre-data-source objects used in ATT&CK.",
                        schema=schema_base+"scos/data-source.json",
                        version="1.0",
                        extension_types=[
                            "new-sco"
                        ],
                        object_marking_refs=S2E_MARKING_REFS
                    )

### Weakness SMO

weakness_ExtensionDefinitionSMO = ExtensionDefinition(
                        id="extension-definition--" + str(uuid.uuid5(namespace, f"weakness")), # extension-definition--31725edc-7d81-5db7-908a-9134f322284a
                        created_by_ref=DOGESEC_IDENTITY_REF,
                        created=created,
                        modified=datetime(2020, 1, 1, tzinfo=UTC),
                        name="Weakness",
                        description="This extension creates a new SDO that can be used to represent weaknesses (for CWEs).",
                        schema=schema_base+"sdos/weakness.json",
                        version="1.0",
                        extension_types=[
                            "new-sdo"
                        ],
                        object_marking_refs=S2E_MARKING_REFS
                    )

### Exploit SMO

exploit_ExtensionDefinitionSMO = ExtensionDefinition(
                        id="extension-definition--" + str(uuid.uuid5(namespace, f"exploit")), # extension-definition--5a047f57-0149-59b6-a079-e2d7c7ac799a
                        created_by_ref=DOGESEC_IDENTITY_REF,
                        created=created,
                        modified=datetime(2020, 1, 1, tzinfo=UTC),
                        name="Exploit",
                        description="This extension creates a new SDO that can be used to represent exploits (of CVEs).",
                        schema=schema_base+"sdos/exploit.json",
                        version="1.0",
                        extension_types=[
                            "new-sdo"
                        ],
                        object_marking_refs=S2E_MARKING_REFS
                    )

### Payment Card SMO

payment_card_ExtensionDefinitionSMO = ExtensionDefinition(
                        id="extension-definition--" + str(uuid.uuid5(namespace, f"payment-card")), # extension-definition--
                        created_by_ref=DOGESEC_IDENTITY_REF,
                        created=created,
                        modified=datetime(2020, 1, 1, tzinfo=UTC),
                        name="Payment Card",
                        description="This extension creates a new SCO that can be used to represent different types of payment card.",
                        schema=schema_base+"scos/payment-card.json",
                        version="1.0",
                        extension_types=[
                            "new-sco"
                        ],
                        object_marking_refs=S2E_MARKING_REFS
                    )

### User Agent SMO

user_agent_ExtensionDefinitionSMO = ExtensionDefinition(
                        id="extension-definition--" + str(uuid.uuid5(namespace, f"user-agent")), # extension-definition--7ca5afee-0e4e-5813-b643-de51538658cc
                        created_by_ref=DOGESEC_IDENTITY_REF,
                        created=created,
                        modified=datetime(2020, 1, 1, tzinfo=UTC),
                        name="User Agent",
                        description="This extension creates a new SCO that can be used to represent user agents used in HTTP request. It is designed to be used when the Network Traffic SCO with HTTP request extension cannot be used due to lack of request information needed for the required properties.",
                        schema=schema_base+"scos/user-agent.json",
                        version="1.0",
                        extension_types=[
                            "new-sco"
                        ],
                        object_marking_refs=S2E_MARKING_REFS
                    )

### Cryptocurrency Wallet SMO

cryptocurrency_wallet_ExtensionDefinitionSMO = ExtensionDefinition(
                        id="extension-definition--" + str(uuid.uuid5(namespace, f"cryptocurrency-wallet")), # extension-definition--be78509e-6958-51b1-8b26-d17ee0eba2d7
                        created_by_ref=DOGESEC_IDENTITY_REF,
                        created=created,
                        modified=datetime(2020, 1, 1, tzinfo=UTC),
                        name="Cryptocurrency Wallet",
                        description="This extension creates a new SCO that can be used to represent cryptocurrency wallets.",
                        schema=schema_base+"scos/cryptocurrency-wallet.json",
                        version="1.0",
                        extension_types=[
                            "new-sco"
                        ],
                        object_marking_refs=S2E_MARKING_REFS
                    )

### Bank Account SMO

bank_account_ExtensionDefinitionSMO = ExtensionDefinition(
                        id="extension-definition--" + str(uuid.uuid5(namespace, f"bank-account")), # extension-definition--f19f3291-6a84-5674-b311-d75a925d5bd9
                        created_by_ref=DOGESEC_IDENTITY_REF,
                        created=created,
                        modified=datetime(2020, 1, 1, tzinfo=UTC),
                        name="Bank Account",
                        description="This extension creates a new SCO that can be used to represent bank account details.",
                        schema=schema_base+"scos/bank-account.json",
                        version="1.0",
                        extension_types=[
                            "new-sco"
                        ],
                        object_marking_refs=S2E_MARKING_REFS
                    )

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

### Indicator Sigma Rule Extension SMO

indicator_sigma_rule_ExtensionDefinitionSMO = ExtensionDefinition(
                        id="extension-definition--" + str(uuid.uuid5(namespace, f"indicator-sigma-rule")), # extension-definition--
                        created_by_ref=DOGESEC_IDENTITY_REF,
                        created=created,
                        modified=datetime(2020, 1, 1, tzinfo=UTC),
                        name="Indicator SDO Sigma Rule Properties",
                        description="This extension adds new properties to Indicator SDOs to capture Sigma Rule specific data.",
                        schema=schema_base+"properties/indicator-sigma-rule.json",
                        version="1.0",
                        extension_types=[
                            "toplevel-property-extension"
                        ],
                        extension_properties=[
                            "x_sigma_type",
                            "x_sigma_level",
                            "x_sigma_status",
                            "x_sigma_license",
                            "x_sigma_fields",
                            "x_sigma_falsepositives",
                            "x_sigma_scope"
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

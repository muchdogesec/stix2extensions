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

created_by_ref="identity--" + str(uuid.uuid5(namespace, f"dogesec"))
created="2020-01-01T00:00:00.000Z"
modified="2020-01-01T00:00:00.000Z"
schema_base="https://raw.githubusercontent.com/muchdogesec/stix2extensions/main/schemas/"

### mitre TLP:CLEAR and stix4doge

object_marking_refs=[
    "marking-definition--94868c89-83c2-464b-929b-a1a8aa3c8487", # this is TLP:CLEAR
    "marking-definition--" + str(uuid.uuid5(namespace, f"stix2extensions")) # 
]

# Create New Extension Defintion SMO
## https://stix2.readthedocs.io/en/latest/api/v21/stix2.v21.common.html

### Phone number SMO

phone_number_ExtensionDefinitionSMO = ExtensionDefinition(
                        id="extension-definition--" + str(uuid.uuid5(namespace, f"phone-number")), # extension-definition--14a97ee2-e666-5ada-a6bd-b7177f79e211
                        created_by_ref=created_by_ref,
                        created=created,
                        modified=modified,
                        name="Phone Number",
                        description="This extension creates a new SCO that can be used to represent phone numbers.",
                        schema=schema_base+"scos/phone-number.json",
                        version="1.0",
                        extension_types=[
                            "new-sco"
                        ],
                        object_marking_refs=object_marking_refs
                    )

### Cryptocurrency Transaction SMO

cryptocurrency_transaction_ExtensionDefinitionSMO = ExtensionDefinition(
                        id="extension-definition--" + str(uuid.uuid5(namespace, f"cryptocurrency-transaction")), # extension-definition--151d042d-4dcf-5e44-843f-1024440318e5
                        created_by_ref=created_by_ref,
                        created=created,
                        modified=modified,
                        name="Cryptocurrency Transaction",
                        description="This extension creates a new SCO that can be used to represent cryptocurrency transactions.",
                        schema=schema_base+"scos/cryptocurrency-transaction.json",
                        version="1.0",
                        extension_types=[
                            "new-sco"
                        ],
                        object_marking_refs=object_marking_refs
                    )

### Weakness SMO

weakness_ExtensionDefinitionSMO = ExtensionDefinition(
                        id="extension-definition--" + str(uuid.uuid5(namespace, f"weakness")), # extension-definition--31725edc-7d81-5db7-908a-9134f322284a
                        created_by_ref=created_by_ref,
                        created=created,
                        modified=modified,
                        name="Weakness",
                        description="This extension creates a new SDO that can be used to represent weaknesses (for CWEs).",
                        schema=schema_base+"sdos/weakness.json",
                        version="1.0",
                        extension_types=[
                            "new-sdo"
                        ],
                        object_marking_refs=object_marking_refs
                    )

### Bank Card SMO

bank_card_ExtensionDefinitionSMO = ExtensionDefinition(
                        id="extension-definition--" + str(uuid.uuid5(namespace, f"bank-card")), # extension-definition--7922f91a-ee77-58a5-8217-321ce6a2d6e0
                        created_by_ref=created_by_ref,
                        created=created,
                        modified=modified,
                        name="Bank Card",
                        description="This extension creates a new SCO that can be used to represent bank cards.",
                        schema=schema_base+"scos/bank-card.json",
                        version="1.0",
                        extension_types=[
                            "new-sco"
                        ],
                        object_marking_refs=object_marking_refs
                    )

### User Agent SMO

user_agent_ExtensionDefinitionSMO = ExtensionDefinition(
                        id="extension-definition--" + str(uuid.uuid5(namespace, f"user-agent")), # extension-definition--7ca5afee-0e4e-5813-b643-de51538658cc
                        created_by_ref=created_by_ref,
                        created=created,
                        modified=modified,
                        name="User Agent",
                        description="This extension creates a new SCO that can be used to represent user agents used in HTTP request. It is designed to be used when the Network Traffic SCO with HTTP request extension cannot be used due to lack of request information needed for the required properties.",
                        schema=schema_base+"scos/user-agent.json",
                        version="1.0",
                        extension_types=[
                            "new-sco"
                        ],
                        object_marking_refs=object_marking_refs
                    )

### Cryptocurrency Wallet SMO

cryptocurrency_wallet_ExtensionDefinitionSMO = ExtensionDefinition(
                        id="extension-definition--" + str(uuid.uuid5(namespace, f"cryptocurrency-wallet")), # extension-definition--be78509e-6958-51b1-8b26-d17ee0eba2d7
                        created_by_ref=created_by_ref,
                        created=created,
                        modified=modified,
                        name="Cryptocurrency Wallet",
                        description="This extension creates a new SCO that can be used to represent cryptocurrency wallets.",
                        schema=schema_base+"scos/cryptocurrency-wallet.json",
                        version="1.0",
                        extension_types=[
                            "new-sco"
                        ],
                        object_marking_refs=object_marking_refs
                    )

### Bank Account SMO

bank_account_ExtensionDefinitionSMO = ExtensionDefinition(
                        id="extension-definition--" + str(uuid.uuid5(namespace, f"bank-account")), # extension-definition--f19f3291-6a84-5674-b311-d75a925d5bd9
                        created_by_ref=created_by_ref,
                        created=created,
                        modified=modified,
                        name="Bank Account",
                        description="This extension creates a new SCO that can be used to represent bank account details.",
                        schema=schema_base+"scos/bank-account.json",
                        version="1.0",
                        extension_types=[
                            "new-sco"
                        ],
                        object_marking_refs=object_marking_refs
                    )

### Vulnerability Scoring Extension SMO

vulnerability_scoring_ExtensionDefinitionSMO = ExtensionDefinition(
                        id="extension-definition--" + str(uuid.uuid5(namespace, f"vulnerability-scoring")), # extension-definition--2c5c13af-ee92-5246-9ba7-0b958f8cd34a
                        created_by_ref=created_by_ref,
                        created=created,
                        modified=modified,
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
                        object_marking_refs=object_marking_refs
                    )

### Indicator Vulnerable CPEs Extension SMO

indicator_vulnerable_cpes_ExtensionDefinitionSMO = ExtensionDefinition(
                        id="extension-definition--" + str(uuid.uuid5(namespace, f"indicator-vulnerable-cpes")), # extension-definition--ad995824-2901-5f6e-890b-561130a239d4
                        created_by_ref=created_by_ref,
                        created=created,
                        modified=modified,
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
                        object_marking_refs=object_marking_refs
                    )

### Report EPSS Scoring SMO

report_epss_scoring_ExtensionDefinitionSMO = ExtensionDefinition(
                        id="extension-definition--" + str(uuid.uuid5(namespace, f"report-epss-scoring")), # extension-definition--f80cce10-5ac0-58d1-9e7e-b4ed0cc4dbb9
                        created_by_ref=created_by_ref,
                        created=created,
                        modified=modified,
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
                        object_marking_refs=object_marking_refs
                    )

### Software CPE SMO

software_cpe_properties_ExtensionDefinitionSMO = ExtensionDefinition(
                        id="extension-definition--" + str(uuid.uuid5(namespace, f"software-cpe-properties")), # extension-definition--82cad0bb-0906-5885-95cc-cafe5ee0a500
                        created_by_ref=created_by_ref,
                        created=created,
                        modified=modified,
                        name="Software SCO CPE Properties",
                        description="This extension adds new properties to Software SCOs to capture CPE data.",
                        schema=schema_base+"properties/software-cpe-properties.json",
                        version="1.0",
                        extension_types=[
                            "toplevel-property-extension"
                        ],
                        extension_properties=[
                            "x_cpe_struct"
                        ],
                        object_marking_refs=object_marking_refs
                    )

attack_flow_ExtensionDefinitionSMO = ExtensionDefinition(
                        type="extension-definition",
                        id="extension-definition--fb9c968a-745b-4ade-9b25-c324172197f4",
                        spec_version="2.1",
                        created="2022-08-02T19:34:35.143Z",
                        modified="2022-08-02T19:34:35.143Z",
                        name="Attack Flow",
                        description="Extends STIX 2.1 with features to create Attack Flows.",
                        created_by_ref="identity--fb9c968a-745b-4ade-9b25-c324172197f4",
                        schema="https://center-for-threat-informed-defense.github.io/attack-flow/stix/attack-flow-schema-2.0.0.json",
                        version="2.0.0",
                        extension_types=["new-sdo"],
                        external_references=[
                            {
                                "source_name": "Documentation",
                                "description": "Documentation for Attack Flow",
                                "url": "https://center-for-threat-informed-defense.github.io/attack-flow",
                            },
                            {
                                "source_name": "GitHub",
                                "description": "Source code repository for Attack Flow",
                                "url": "https://github.com/center-for-threat-informed-defense/attack-flow",
                            },
                        ],
                    )

import uuid
from uuid import UUID

from stix2 import Indicator
from stix2extensions.definitions.properties import (
    IndicatorSigmaRulePropertyExtension,
)

indicator_sigma_rule_ExtensionDefinitionSMO = (
    IndicatorSigmaRulePropertyExtension.extension_definition
)

# define UUID for generating UUIDv5s -- use stix2extensions namespace as this is an SDO
namespace = UUID("1abb62b9-e513-5f55-8e73-8f6d7b55c237")

# define values that are recycled between objects
created_by_ref = "identity--" + str(uuid.uuid5(namespace, f"dogesec-demo"))
created = "2021-09-12T00:00:00.000Z"
modified = "2022-10-09T00:00:00.000Z"

example_IndicatorSDO = Indicator(
    id="indicator--330e2030-1dc2-45e6-be13-9342b102621b",
    created_by_ref=created_by_ref,
    created=created,
    modified=modified,
    valid_from=created,
    name="Okta Policy Modified or Deleted",
    description="Detects when an Okta policy is modified or deleted.",
    pattern=(
        "id: 6a4c842a-986f-43f0-8f3f-d98cdd36e01e\n"
        "title: Okta Policy Modified or Deleted\n"
        "description: Detects when an Okta policy is modified or deleted.\n"
        "level: medium\n"
        "status: stable\n"
    ),
    pattern_type="sigma",
    x_sigma_type="base",
    x_sigma_level="medium",
    x_sigma_status="stable",
    object_marking_refs=[
        "marking-definition--94868c89-83c2-464b-929b-a1a8aa3c8487",
        "marking-definition--" + str(uuid.uuid5(namespace, f"stix2extensions")),
    ],
    extensions={
        indicator_sigma_rule_ExtensionDefinitionSMO.id: {
            "extension_type": "toplevel-property-extension",
        }
    },
)

examples = [
    example_IndicatorSDO,
]

import uuid
from uuid import UUID

from stix2 import Identity
from stix2extensions.definitions.properties import (
    IdentityOpenCTIPropertyExtension,
)

identity_opencti_ExtensionDefinitionSMO = (
    IdentityOpenCTIPropertyExtension.extension_definition
)

# define UUID for generating UUIDv5s -- use stix2extensions namespace as this is an SDO
namespace = UUID("1abb62b9-e513-5f55-8e73-8f6d7b55c237")

# define values that are recycled between objects
created_by_ref = "identity--" + str(uuid.uuid5(namespace, f"dogesec-demo"))
created = "2020-01-01T00:00:00.000Z"
modified = "2020-01-01T00:00:00.000Z"

# Create Identity SDO object

example_IdentitySDO = Identity(
    id="identity--" + str(uuid.uuid5(namespace, f"example_IdentitySDO")),
    created_by_ref=created_by_ref,
    created=created,
    modified=modified,
    name="Agriculture and agribusiness",
    description=(
        "Private entities specialized in the growth, culture, transport and transformation "
        "of plants or livestock for food."
    ),
    identity_class="class",
    x_opencti_aliases=[
        "Agriculture",
        "Agribusiness",
        "Food Production",
        "Nutritional Supplements",
    ],
    object_marking_refs=[
        "marking-definition--94868c89-83c2-464b-929b-a1a8aa3c8487",
        "marking-definition--" + str(uuid.uuid5(namespace, f"stix2extensions")),
    ],
    extensions={
        identity_opencti_ExtensionDefinitionSMO.id: {
            "extension_type": "toplevel-property-extension",
        }
    },
)

examples = [
    example_IdentitySDO,
]

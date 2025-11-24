import uuid
from uuid import UUID

from stix2 import Location
from stix2extensions.definitions.properties import (
    LocationOpenCTIPropertyExtension,
)

location_opencti_ExtensionDefinitionSMO = (
    LocationOpenCTIPropertyExtension.extension_definition
)

# define UUID for generating UUIDv5s -- use stix2extensions namespace as this is an SDO
namespace = UUID("1abb62b9-e513-5f55-8e73-8f6d7b55c237")

# define values that are recycled between objects
created_by_ref = "identity--" + str(uuid.uuid5(namespace, f"dogesec-demo"))
created = "2020-01-01T00:00:00.000Z"
modified = "2020-01-01T00:00:00.000Z"

# Create Location SDO object

example_opencti_LocationSDO = Location(
    id="location--" + str(uuid.uuid5(namespace, f"example_opencti_LocationSDO")),
    created_by_ref=created_by_ref,
    created=created,
    modified=modified,
    name="Egypt",
    country="EG",
    x_opencti_aliases=["EGY", "EG"],
    x_opencti_location_type="Country",
    latitude=26.820553,
    longitude=30.802498,
    region="northern-africa",
    external_references=[
        {"source_name": "location2stix", "external_id": "EG"},
        {"source_name": "type", "external_id": "country"},
        {"source_name": "alpha-2", "external_id": "EG"},
        {"source_name": "alpha-3", "external_id": "EGY"},
        {"source_name": "iso_3166-2", "external_id": "ISO 3166-2:EG"},
        {"source_name": "country-code", "external_id": "818"},
    ],
    object_marking_refs=[
        "marking-definition--94868c89-83c2-464b-929b-a1a8aa3c8487",
        "marking-definition--" + str(uuid.uuid5(namespace, f"stix2extensions")),
    ],
    extensions={
        location_opencti_ExtensionDefinitionSMO.id: {
            "extension_type": "toplevel-property-extension"
        }
    },
)

examples = [
    example_opencti_LocationSDO,
]

from stix2.properties import (
    StringProperty,
    EnumProperty,
)

from stix2extensions.automodel import (
    AutomodelExtensionBase,
    automodel,
    extend_property,
)
from stix2extensions.automodel.property_extension import (
    CustomPropertyExtension,
    ExtensionTypes,
)


@automodel
@CustomPropertyExtension(
    "location-opencti",
    [
        (
            "x_opencti_aliases",
            extend_property(
                StringProperty(),
                description="Two and three letter country code for the Country. Only used for Country location types",
                examples=["US", "USA"],
            ),
        ),
        (
            "x_opencti_location_type",
            extend_property(
                EnumProperty(allowed=["Country", "Region"]),
                description="The type of location",
            ),
        ),
    ],
    extension_type=ExtensionTypes.TOPLEVEL_PROPERTY_EXTENSION,
)
class LocationOpenCTIPropertyExtension(AutomodelExtensionBase):
    base_schema_ref = "https://raw.githubusercontent.com/oasis-open/cti-stix2-json-schemas/master/schemas/sdos/location.json"
    extension_description = (
        "This extension adds OpenCTI-specific properties to STIX Location SDOs."
    )

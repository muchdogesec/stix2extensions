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
    "identity-opencti",
    [
        (
            "x_opencti_aliases",
            extend_property(
                extend_property(StringProperty(), examples=["Agriculture", "Agribusiness", "Food Production", "Nutritional Supplements"]),
                description="A list of aliases used by OpenCTI",
            ),
        ),
    ],
    extension_type=ExtensionTypes.TOPLEVEL_PROPERTY_EXTENSION,
)
class IdentityOpenCTIPropertyExtension(AutomodelExtensionBase):
    base_schema_ref = "https://raw.githubusercontent.com/oasis-open/cti-stix2-json-schemas/master/schemas/sdos/identity.json"
    extension_description = "This extension adds new properties to Identity SDOs to capture OpenCTI specific data."

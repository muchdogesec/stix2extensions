from typing import OrderedDict
from stix2.v21.base import _STIXBase21
from stix2.properties import (
    ListProperty,
    EmbeddedObjectProperty,
    StringProperty,
    BooleanProperty,
    EnumProperty,
    TimestampProperty,
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


class CPEStruct(AutomodelExtensionBase, _STIXBase21):
    _properties = OrderedDict(
        [
            (
                "cpe_version",
                extend_property(
                    StringProperty(),
                    description="The version of the CPE definition. The latest CPE definition version is 2.3.",
                    examples=["2.3"],
                ),
            ),
            (
                "part",
                extend_property(
                    EnumProperty(allowed=["a", "h", "o"]),
                    description="May have 1 of 3 values: `a` for Applications, `h` for Hardware, `o` for Operating Systems",
                ),
            ),
            (
                "vendor",
                extend_property(
                    StringProperty(),
                    description="Values for this attribute SHOULD describe or identify the person or organization that manufactured or created the product.",
                    examples=["google"],
                ),
            ),
            (
                "product",
                extend_property(
                    StringProperty(),
                    description="The name of the system/package/component. `product` and `vendor` are sometimes identical. It can not contain spaces, slashes, or most special characters.",
                    examples=["chrome"],
                ),
            ),
            (
                "version",
                extend_property(
                    StringProperty(),
                    description="Vendor-specific alphanumeric string characterizing the particular release version of the product.",
                    examples=["9.0.597.63"],
                ),
            ),
            (
                "update",
                extend_property(
                    StringProperty(),
                    description="Vendor-specific alphanumeric strings characterizing the particular update, service pack, or point release of the product.",
                    examples=["*"],
                ),
            ),
            (
                "edition",
                extend_property(
                    StringProperty(),
                    description="A further granularity describing the build of the system/package/component, beyond `version`.",
                    examples=["*"],
                ),
            ),
            (
                "language",
                extend_property(
                    StringProperty(),
                    description="A valid language tag as defined by IETF RFC 4646 entitled Tags for Identifying Languages.",
                    examples=["*"],
                ),
            ),
            (
                "sw_edition",
                extend_property(
                    StringProperty(),
                    description="How the product is tailored to a particular market or class of end users.",
                    examples=["*"],
                ),
            ),
            (
                "target_sw",
                extend_property(
                    StringProperty(),
                    description="Software computing environment within which the product operates.",
                    examples=["*"],
                ),
            ),
            (
                "target_hw",
                extend_property(
                    StringProperty(),
                    description="Instruction set architecture (e.g., x86) on which the product operates.",
                    examples=["*"],
                ),
            ),
            (
                "other",
                extend_property(
                    StringProperty(),
                    description="Any other general descriptive or identifying information which is vendor- or product-specific and which does not logically fit anywhere else.",
                    examples=["*"],
                ),
            ),
        ]
    )


@automodel
@CustomPropertyExtension(
    "software-cpe-properties",
    [
        (
            "x_cpe_struct",
            extend_property(
                EmbeddedObjectProperty(type=CPEStruct),
                description="Expanded struct of CPE values.",
            ),
        ),
        (
            "x_revoked",
            extend_property(
                BooleanProperty(),
                description="The revoked property indicates whether the object has been revoked.",
                examples=[True],
            ),
        ),
        (
            "x_created",
            extend_property(
                TimestampProperty(),
                description="The created property represents the time at which the first version of this object was created. Must be precise to the nearest millisecond.",
                examples=["2020-01-01T00:00:00.000Z"],
            ),
        ),
        (
            "x_modified",
            extend_property(
                TimestampProperty(),
                description="The modified property represents the time that this particular version of the object was modified. Must be precise to the nearest millisecond.",
                examples=["2020-01-01T00:00:00.000Z"],
            ),
        ),
    ],
    extension_type=ExtensionTypes.TOPLEVEL_PROPERTY_EXTENSION,
)
class SoftwareCpePropertiesExtension(AutomodelExtensionBase):
    base_schema_ref = "https://raw.githubusercontent.com/oasis-open/cti-stix2-json-schemas/master/schemas/observables/software.json"
    extension_description = "This extension adds new properties to Software SCOs to capture full CPE information."

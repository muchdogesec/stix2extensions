from stix2.properties import StringProperty, EnumProperty, ListProperty

from stix2extensions.automodel import (
    AutomodelExtensionBase,
    automodel,
    extend_property,
    CustomPropertyExtension,
    ExtensionTypes,
)


@automodel
@CustomPropertyExtension(
    "indicator-sigma-rule",
    [
        (
            "x_sigma_type",
            extend_property(
                EnumProperty(allowed=["base", "correlation"]),
                description="The type of Sigma Rule",
            ),
        ),
        (
            "x_sigma_level",
            extend_property(
                EnumProperty(
                    allowed=["informational", "low", "medium", "high", "critical"]
                ),
                description="The level field contains one of five string values. It describes the criticality of a triggered rule.",
            ),
        ),
        (
            "x_sigma_status",
            extend_property(
                EnumProperty(
                    allowed=[
                        "stable",
                        "test",
                        "experimental",
                        "deprecated",
                        "unsupported",
                    ]
                ),
                description="Declares the status of the rule.",
            ),
        ),
        (
            "x_sigma_license",
            extend_property(
                StringProperty(),
                description="License of the rule according the SPDX ID specification.",
                examples=["mit", "0BSD"],
            ),
        ),
        (
            "x_sigma_falsepositives",
            extend_property(
                ListProperty(
                    extend_property(
                        StringProperty(),
                        examples=[
                            "Verify whether the user identity, user agent, and/or hostname should be making changes in your environment."
                        ],
                    )
                ),
                description="A list of known false positives that may occur.",
            ),
        ),
        (
            "x_sigma_fields",
            extend_property(
                ListProperty(StringProperty()),
                description="A list of log fields that could be interesting in further analysis of the event and should be displayed to the analyst.",
                examples=[["Image", "CommandLine", "ParentImage"]],
            ),
        ),
        (
            "x_sigma_scope",
            extend_property(
                ListProperty(StringProperty()),
                description="A list of the intended scopes of the rule. This would allow you to define if a rule is meant to trigger on specific set of types of machines that might have a specific software installed.",
                examples=[["server"]],
            ),
        ),
    ],
    extension_type=ExtensionTypes.TOPLEVEL_PROPERTY_EXTENSION,
)
class IndicatorSigmaRulePropertyExtension(AutomodelExtensionBase):
    base_schema_ref = "https://raw.githubusercontent.com/oasis-open/cti-stix2-json-schemas/master/schemas/sdos/indicator.json"
    extension_description = "This extension adds new properties to Indicator SDOs to capture Sigma Rule specific data."

from typing import OrderedDict
from stix2.v21.base import _STIXBase21
from stix2.properties import (
    ListProperty,
    EmbeddedObjectProperty,
    StringProperty,
    ReferenceProperty,
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


class SoftwareCriteria(AutomodelExtensionBase, _STIXBase21):
    _properties = OrderedDict(
        [
            (
                "criteria",
                extend_property(
                    StringProperty(required=True),
                    description="The criteria for the CPE",
                    examples=["cpe:2.3:a:dell:powerscale_onefs:9.1.0:*:*:*:*:*:*:*"],
                ),
            ),
            (
                "matchCriteriaId",
                extend_property(
                    StringProperty(required=True),
                    description="The matchCriteriaId for the CPE",
                    examples=["68291D44-DBE1-4923-A848-04E64288DC23"],
                ),
            ),
            (
                "match_criteria_ref",
                extend_property(
                    ReferenceProperty(valid_types=["grouping"]),
                    description="The STIX ID for the grouping associated with this criteria",
                    examples=["grouping--01234567-89ab-cdef-0123-456789abcdef"],
                ),
            ),
        ]
    )


class SoftwareCriteriaList(AutomodelExtensionBase, _STIXBase21):
    _properties = OrderedDict(
        [
            (
                "vulnerable",
                extend_property(
                    ListProperty(EmbeddedObjectProperty(SoftwareCriteria)),
                    description="List of CPE Matches that are vulnerable",
                ),
            ),
            (
                "not_vulnerable",
                extend_property(
                    ListProperty(EmbeddedObjectProperty(SoftwareCriteria)),
                    description="List of CPE Matches that are NOT vulnerable",
                ),
            ),
        ]
    )


@automodel
@CustomPropertyExtension(
    "indicator-vulnerable-cpes",
    [
        (
            "x_cpes",
            extend_property(
                EmbeddedObjectProperty(type=SoftwareCriteriaList),
                description="List of CPE entries including vulnerable and not vulnerable objects.",
            ),
        ),
    ],
    extension_type=ExtensionTypes.TOPLEVEL_PROPERTY_EXTENSION,
)
class IndicatorVulnerableCPEPropertyExtension(AutomodelExtensionBase):
    base_schema_ref = "https://raw.githubusercontent.com/oasis-open/cti-stix2-json-schemas/master/schemas/sdos/indicator.json"
    extension_description = "This extension adds new properties to Indicator SDOs to list CPE vulnerable inside a pattern."

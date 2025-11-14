from typing import OrderedDict
from stix2.v21.base import _STIXBase21
from stix2.properties import (
    ListProperty,
    EmbeddedObjectProperty,
    StringProperty,
    FloatProperty,
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


class EpssStruct(AutomodelExtensionBase, _STIXBase21):
    _properties = OrderedDict(
        [
            (
                "date",
                extend_property(
                    StringProperty(),
                    description="The date of the EPSS score in the format YYYY-MM-DD",
                    examples=["2020-01-01"],
                    pattern=r"^\d{4}-\d{2}-\d{2}$",
                ),
            ),
            (
                "score",
                extend_property(
                    FloatProperty(min=0, max=1),
                    description="EPSS score (0.0 - 1.0) estimating probability of exploitation.",
                    examples=[0.11],
                ),
            ),
            (
                "percentile",
                extend_property(
                    FloatProperty(min=0, max=1),
                    description="EPSS percentile (0.0 - 1.0) relative to other vulnerabilities.",
                    examples=[0.89],
                ),
            ),
        ]
    )


@automodel
@CustomPropertyExtension(
    "report-epss-scoring",
    [
        (
            "x_epss",
            extend_property(
                ListProperty(EmbeddedObjectProperty(type=EpssStruct)),
                description="List of EPSS score entries with date, score, and percentile.",
            ),
        ),
    ],
    extension_type=ExtensionTypes.TOPLEVEL_PROPERTY_EXTENSION,
)
class ReportEPSSScoring(AutomodelExtensionBase):
    base_schema_ref = "https://raw.githubusercontent.com/oasis-open/cti-stix2-json-schemas/master/schemas/sdos/report.json"
    extension_description = "This extension adds new properties to Report SDOs to capture EPSS scores for CVEs."

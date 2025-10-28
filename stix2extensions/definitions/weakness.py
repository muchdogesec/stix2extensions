from enum import StrEnum
from stix2 import CustomObject
from stix2.properties import (
    ListProperty,
    StringProperty,
    OpenVocabProperty,
    EnumProperty,
)

from stix2extensions.automodel.automodel import auto_model, extend_property


_type = "weakness"


VOCAB__DETECTION_METHODS = [
    "Manual Analysis",
    "Automated Analysis",
    "Automated Static Analysis - Source Code",
    "Simulation / Emulation",
    "Formal Verification",
    "Fuzzing",
    "Automated Static Analysis",
    "Dynamic Analysis with Manual Results Interpretation",
    "Dynamic Analysis with Automated Results Interpretation",
    "Architecture or Design Review",
    "Manual Static Analysis - Source Code",
    "Automated Dynamic Analysis",
    "Manual Static Analysis - Binary or Bytecode",
    "Automated Static Analysis - Binary or Bytecode",
    "Black Box",
    "White Box",
    "Manual Static Analysis",
    "Other",
    "Manual Dynamic Analysis",
]

VOCAB__MODES_OF_INTRODUCTION = [
    "Architecture and Design",
    "Implementation",
    "System Configuration",
    "Requirements",
    "Operation",
    "Patching and Maintenance",
    "Manufacturing",
    "Installation",
    "Integration",
    "Bundling",
    "Build and Compilation",
    "Policy",
    "Documentation",
    "Testing",
    "Distribution",
]

VOCAB__COMMON_CONSEQUENCES = [
    "Confidentiality",
    "Integrity",
    "Availability",
    "Authentication",
    "Authorization",
    "Other",
    "Access Control",
    "Non-Repudiation",
    "Accountability",
]


class COMMON_CONSEQUENCES_OV(StrEnum):
    Confidentiality = "Confidentiality"
    Integrity = "Integrity"
    Availability = "Availability"
    Authentication = "Authentication"
    Authorization = "Authorization"
    Other = "Other"
    Access_Control = "Access Control"
    Non_Repudiation = "Non-Repudiation"
    Accountability = "Accountability"


@auto_model
@CustomObject(
    "weakness",
    [
        (
            "name",
            extend_property(
                StringProperty(required=True),
                description="Name of the weakness as defined in CWE",
                examples=["Buffer Overflow", "SQL Injection"],
            ),
        ),
        (
            "description",
            extend_property(
                StringProperty(),
                description="Detailed description of the weakness",
                examples=[
                    "A buffer overflow occurs when data exceeds the allocated buffer memory, potentially allowing code execution."
                ],
            ),
        ),
        (
            "modes_of_introduction",
            extend_property(
                ListProperty(
                    extend_property(
                        OpenVocabProperty(allowed=VOCAB__MODES_OF_INTRODUCTION),
                        description="Phase or circumstance in which the weakness may be introduced",
                    )
                ),
                description="Ways in which the weakness can be introduced into software or systems",
            ),
        ),
        (
            "likelihood_of_exploit",
            extend_property(
                ListProperty(EnumProperty(allowed=["High", "Medium", "Low"])),
                description="Likelihood that the weakness can be successfully exploited",
            ),
        ),
        (
            "common_consequences",
            extend_property(
                ListProperty(
                    extend_property(
                        OpenVocabProperty(allowed=COMMON_CONSEQUENCES_OV),
                        description="Typical impact categories resulting from exploitation of this weakness.",
                    )
                ),
                description="Typical impacts or consequences resulting from the weakness",
            ),
        ),
        (
            "detection_methods",
            extend_property(
                ListProperty(OpenVocabProperty(allowed=VOCAB__DETECTION_METHODS)),
                description="Methods or techniques used to detect this weakness",
            ),
        ),
    ],
)
class Weakness(object):
    pass

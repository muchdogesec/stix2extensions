from stix2 import CustomObject
from stix2.properties import (
    ReferenceProperty,
    ListProperty,
    StringProperty,
)

from stix2extensions.automodel import extend_property, automodel

_type = "attack-flow"


@automodel
@CustomObject(
    _type,
    [
        (
            "name",
            extend_property(
                StringProperty(required=True),
                description="Unique name of the attack flow, representing a sequence of related attack actions",
            ),
        ),
        (
            "description",
            extend_property(
                StringProperty(),
                description="Detailed description of the attack flow, including its purpose and impact",
            ),
        ),
        (
            "scope",
            extend_property(
                StringProperty(required=True),
                description="Scope or environment in which this attack flow is applicable, e.g., enterprise network, cloud",
            ),
        ),
        (
            "start_refs",
            extend_property(
                ListProperty(ReferenceProperty(valid_types=["attack-action"])),
                description="References to the initial attack-action(s) that start this attack flow",
            ),
        ),
    ],
    extension_name="extension-definition--fb9c968a-745b-4ade-9b25-c324172197f4",
)
class AttackFlow(object):
    pass


_type = "attack-action"


@CustomObject(
    _type,
    [
        (
            "technique_id",
            extend_property(
                StringProperty(required=True),
                description="Identifier of the ATT&CK technique used in this action",
                examples=["T1003.008", "T1548"],
            ),
        ),
        (
            "technique_ref",
            extend_property(
                ReferenceProperty(
                    required=True, valid_types=["attack-pattern", "x-mitre-tactic"]
                ),
                description="STIX reference to the corresponding technique or tactic object",
                examples=[
                    "attack-pattern--d0b4fcdb-d67d-4ed2-99ce-788b12f8c0f4",
                    "attack-pattern--67720091-eee3-4d2d-ae16-8264567f6f5b",
                ],
            ),
        ),
        (
            "tactic_id",
            extend_property(
                StringProperty(required=True),
                description="Identifier of the ATT&CK tactic associated with this action",
                examples=["TA0005"],
            ),
        ),
        (
            "tactic_ref",
            extend_property(
                ReferenceProperty(required=True, valid_types=["x-mitre-tactic"]),
                description="STIX reference to the associated tactic",
                examples=["x-mitre-tactic--78b23412-0651-46d7-a540-170a1ce8bd5a"],
            ),
        ),
        (
            "name",
            extend_property(
                StringProperty(required=True),
                description="Descriptive name of the attack action or technique",
            ),
        ),
        (
            "effect_refs",
            extend_property(
                ListProperty(ReferenceProperty(valid_types=["attack-action"])),
                description="References to subsequent attack-actions that are caused or influenced by this action",
            ),
        ),
    ],
)
class AttackAction(object):
    with_extension = AttackFlow.with_extension

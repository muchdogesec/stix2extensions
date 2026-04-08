from stix2 import CustomObject
from stix2.properties import (
    ReferenceProperty,
    StringProperty,
    ListProperty,
)

from stix2extensions.automodel import AutomodelExtensionBase, automodel, extend_property

_type = "procedure"


@automodel
@CustomObject(
    _type,
    [
        (
            "name",
            extend_property(
                StringProperty(required=True),
                description="A short, recognisable name for the procedural pattern.",
                examples=[
                    "Shadow copy deletion via vssadmin before ransomware deployment"
                ],
            ),
        ),
        (
            "description",
            extend_property(
                StringProperty(),
                description="A plain-language summary of how the procedure is operationalised.",
                examples=[
                    "Uses WMI to spawn PowerShell, deletes shadow copies, and schedules ransomware execution on backup systems."
                ],
            ),
        ),
        (
            "objective",
            extend_property(
                StringProperty(),
                description="The attacker goal or intended effect achieved by the procedure.",
                examples=["Prevent host recovery before ransomware encryption"],
            ),
        ),
        (
            "context",
            extend_property(
                StringProperty(),
                description="The operational context or environment where this procedure is relevant.",
                examples=["Windows backup infrastructure during maintenance windows"],
            ),
        ),
        (
            "variants",
            extend_property(
                ListProperty(StringProperty),
                description="Known variants of the same underlying procedural pattern.",
                examples=[
                    [
                        "Uses WMIC to launch encoded PowerShell",
                        "Uses PsExec before scheduled task creation",
                    ]
                ],
            ),
        ),
        (
            "preconditions",
            extend_property(
                ListProperty(StringProperty),
                description="Conditions that typically need to be true before the procedure succeeds.",
                examples=[
                    [
                        "Administrative access to the target host",
                        "Remote execution over WMI is permitted",
                    ]
                ],
            ),
        ),
        (
            "required_permissions",
            extend_property(
                ListProperty(StringProperty),
                description="The permissions or privileges generally needed to execute the procedure.",
                examples=[
                    [
                        "Local administrator",
                        "Permission to create scheduled tasks",
                    ]
                ],
            ),
        ),
        (
            "targeted_asset_types",
            extend_property(
                ListProperty(StringProperty),
                description="The types of assets typically targeted by this procedure.",
                examples=[
                    [
                        "Windows backup servers",
                        "Recovery infrastructure",
                    ]
                ],
            ),
        ),
        (
            "command_line_ref",
            extend_property(
                 ReferenceProperty(valid_types="process", spec_version="2.1"),
                description="Optional reference to a representative STIX process object showing how the procedure is typically executed.",
                examples=["process--8e6b6156-69f7-4f6c-bf99-100f8b85222d"],
            ),
        ),
    ]
)
class Procedure(AutomodelExtensionBase):
    extension_description = (
        "This extension creates a new SDO that can be used to represent adversary procedures."
    )
import uuid
from uuid import UUID

from stix2extensions.definitions.sdos import Procedure

namespace = UUID("1abb62b9-e513-5f55-8e73-8f6d7b55c237")

created_by_ref = "identity--" + str(uuid.uuid5(namespace, f"dogesec-demo"))
created = "2020-01-01T00:00:00.000Z"
modified = "2020-01-01T00:00:00.000Z"

example_ProcedureSDO = Procedure(
    id="procedure--" + str(uuid.uuid5(namespace, f"A demo procedure")),
    created_by_ref=created_by_ref,
    created=created,
    modified=modified,
    name="Shadow copy deletion via vssadmin before ransomware deployment",
    description="Uses WMI to spawn PowerShell, deletes shadow copies, and schedules ransomware execution on backup systems.",
    objective="Prevent host recovery before ransomware encryption",
    context="Windows backup infrastructure during maintenance windows",
    variants=[
            "Uses WMIC to launch encoded PowerShell",
            "Uses PsExec before scheduled task creation"
    ],
    preconditions=[
            "Administrative access to the target host",
            "Remote execution over WMI is permitted"
    ],
    required_permissions=[
            "Local administrator",
            "Permission to create scheduled tasks"
    ],
    targeted_asset_types=[
            "Windows backup servers",
            "Recovery infrastructure"
    ],
    command_line_ref="process--8e6b6156-69f7-4f6c-bf99-100f8b85222d"
)

examples = [
    example_ProcedureSDO,
]
import uuid
from uuid import UUID

from stix2extensions.definitions.scos import DataSource

namespace = UUID("00abedb4-aa42-466c-9c01-fed23315a9b7")

example_DataSourceSCO = DataSource(
    id="data-source--" + str(uuid.uuid5(namespace, f"Powershell Script")),
    product="windows",
    category="ps_script",
    definition="Script Block Logging must be enabled",
)

examples = [
    example_DataSourceSCO,
]
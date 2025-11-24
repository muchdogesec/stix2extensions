import uuid
from uuid import UUID

from stix2 import Software
from stix2extensions.definitions.properties import (
    SoftwareCpePropertiesExtension,
)

software_cpe_properties_ExtensionDefinitionSMO = (
    SoftwareCpePropertiesExtension.extension_definition
)

namespace = UUID("1abb62b9-e513-5f55-8e73-8f6d7b55c237")

created_by_ref = "identity--" + str(uuid.uuid5(namespace, f"dogesec-demo"))

example_SoftwareSCO = Software(
    id="software--fda5adb5-23e5-5089-a256-36f298ba241f",
    name="EGroupware 14.1.20140710 Community Edition",
    cpe="cpe:2.3:a:egroupware:egroupware:14.1.20140710:*:*:*:community:*:*:*",
    swid="A1F2EAFC-0523-4257-A9EA-94462CA2BDB8",
    languages=["en"],
    vendor="egroupware",
    version="14.1.20140710",
    x_cpe_struct={
        "cpe_version": "2.3",
        "part": "a",
        "vendor": "egroupware",
        "product": "egroupware",
        "version": "14.1.20140710",
        "update": "*",
        "edition": "*",
        "language": "*",
        "sw_edition": "community",
        "target_sw": "*",
        "target_hw": "*",
        "other": "*",
    },
    x_revoked=False,
    x_created="2020-01-01T00:00:00.000Z",
    x_modified="2020-01-01T00:00:00.000Z",
    extensions={
        software_cpe_properties_ExtensionDefinitionSMO.id: {
            "extension_type": "toplevel-property-extension"
        }
    },
)

examples = [
    example_SoftwareSCO,
]

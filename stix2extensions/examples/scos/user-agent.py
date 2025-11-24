import uuid
from uuid import UUID

from stix2extensions.definitions.scos import UserAgent

namespace = UUID("00abedb4-aa42-466c-9c01-fed23315a9b7")
userAgentString = "Mozilla/5.0 (Linux; Android 11; Lenovo YT-J706X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
example_UserAgentSCO = UserAgent(
    id="user-agent--" + str(
        uuid.uuid5(
            namespace,
            userAgentString,
        )
    ),
    value=userAgentString,
)

examples = [
    example_UserAgentSCO,
]
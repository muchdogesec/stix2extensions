from stix2 import CustomObservable
from stix2.properties import (
    StringProperty,
)

from stix2extensions.automodel import AutomodelExtensionBase, automodel, extend_property

_type = "data-source"


@automodel
@CustomObservable(
    _type,
    [
        (
            "category",
            extend_property(
                StringProperty(),
                description="The category value is used to select all log files written by a certain group of products, like firewalls or web server logs.",
                examples=[
                    "ps_script",
                    "process_creation",
                    "network_connection",
                    "file_event",
                ],
            ),
        ),
        (
            "product",
            extend_property(
                StringProperty(),
                description="The product value is used to select all log outputs of a certain product. For example, all Windows Eventlog types including Security, System, Application and the new log types like AppLocker and Windows Defender.",
                examples=["windows", "linux", "nginx", "sysmon"],
            ),
        ),
        (
            "service",
            extend_property(
                StringProperty(),
                description="Use the service value to select only a subset of a product's logs, like the sshd on Linux or the Security Eventlog on Windows systems.",
                examples=["security", "systemd", "sshd", "auditd"],
            ),
        ),
        (
            "definition",
            extend_property(
                StringProperty(),
                description="You may also see a definition field within logsource description. This can also provide more information about how to onboard the log data source correctly, and doesn't get included when completing logsource matching.",
                examples=[
                    "Windows Security Event Logs for authentication and access events"
                ],
            ),
        ),
    ],
    id_contrib_props=["category", "product", "service"],
)
class DataSource(AutomodelExtensionBase):
    extension_description = "This extension creates a new SCO that can be used to represent data sources. Very similar to x-mitre-data-source objects used in ATT&CK."

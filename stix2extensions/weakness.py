
from stix2 import CustomObject
from stix2.properties import (
    ExtensionsProperty, ReferenceProperty,
    IDProperty, ListProperty, StringProperty,
    TimestampProperty, TypeProperty,
)
from stix2.v21.common import (
    ExternalReference,
)
from stix2.utils import NOW
from ._extensions import weakness_ExtensionDefinitionSMO

_type = 'weakness'
@CustomObject('weakness', [
    ('type', TypeProperty(_type, spec_version='2.1')),
    ('spec_version', StringProperty(fixed='2.1')),
    ('id', IDProperty(_type, spec_version='2.1')),
    ('created_by_ref', ReferenceProperty(valid_types='identity', spec_version='2.1')),
    ('created', TimestampProperty(default=lambda: NOW, precision='millisecond', precision_constraint='min')),
    ('modified', TimestampProperty(default=lambda: NOW, precision='millisecond', precision_constraint='min')),
    ('name', StringProperty(required=True)),
    ('description', StringProperty()),
    ('modes_of_introduction', ListProperty(StringProperty)),
    ('likelihood_of_exploit', ListProperty(StringProperty)),
    ('common_consequences', ListProperty(StringProperty)),
    ('detection_methods', ListProperty(StringProperty)),
    ('external_references', ListProperty(ExternalReference)),
    ('object_marking_refs', ListProperty(ReferenceProperty(valid_types='marking-definition', spec_version='2.1'))),
    # ('extensions', ExtensionsProperty(spec_version='2.1'))
], extension_name=weakness_ExtensionDefinitionSMO.id)
class Weakness(object):
    pass
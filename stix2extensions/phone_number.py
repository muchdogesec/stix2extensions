
from stix2 import CustomObservable
from stix2.properties import (
    ExtensionsProperty, ReferenceProperty,
    IDProperty, ListProperty, StringProperty,
    TypeProperty,
)
from ._extensions import phone_number_ExtensionDefinitionSMO

_type = 'phone-number'
@CustomObservable('phone-number', [
    ('type', TypeProperty(_type, spec_version='2.1')),
    ('spec_version', StringProperty(fixed='2.1')),
    ('id', IDProperty(_type, spec_version='2.1')),
    ('number', StringProperty(required=True)),
    ('country', StringProperty()),
    ('connection', StringProperty()),
    ('provider', StringProperty()),
    ('object_marking_refs', ListProperty(ReferenceProperty(valid_types='marking-definition', spec_version='2.1'))),
    # ('extensions', ExtensionsProperty(spec_version='2.1'))
], extension_name=phone_number_ExtensionDefinitionSMO.id, id_contrib_props=['number'])
class Phonenumber(object):
    pass

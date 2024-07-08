
from stix2 import CustomObservable
from stix2.properties import (
    ExtensionsProperty, ReferenceProperty,
    IDProperty, ListProperty, StringProperty,
    TypeProperty,
)

from ._extensions import bank_account_ExtensionDefinitionSMO

_type = 'bank-account'
@CustomObservable('bank-account', [
    ('type', TypeProperty(_type, spec_version='2.1')),
    ('spec_version', StringProperty(fixed='2.1')),
    ('id', IDProperty(_type, spec_version='2.1')),
    ('bank', StringProperty()),
    ('country', StringProperty()),
    ('currency', StringProperty()),
    ('holder_name', StringProperty()),
    ('iban_number', StringProperty(required=True)),
    ('swift_code', StringProperty()),
    ('object_marking_refs', ListProperty(ReferenceProperty(valid_types='marking-definition', spec_version='2.1'))),
    # ('extensions', ExtensionsProperty(spec_version='2.1'))
], extension_name=bank_account_ExtensionDefinitionSMO.id, id_contrib_props=['iban_number'])
class BankAccount(object):
    pass
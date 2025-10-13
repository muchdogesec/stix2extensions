
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
    ('country_ref', ReferenceProperty(valid_types='location', spec_version='2.1')),
    ('currency', StringProperty()),
    ('bank', StringProperty()),
    ('issuer_ref', ReferenceProperty(valid_types='identity', spec_version='2.1')),
    ('holder_ref', ReferenceProperty(valid_types='identity', spec_version='2.1')),
    ('account_number', StringProperty()),
    ('iban', StringProperty()),
    ('bic', StringProperty()),
    # ('extensions', ExtensionsProperty(spec_version='2.1'))
], extension_name=bank_account_ExtensionDefinitionSMO.id, id_contrib_props=['iban', 'account_number', 'country_ref'])
class BankAccount(object):
    def _check_object_constraints(self):
        self._check_at_least_one_property(['iban', 'account_number'])
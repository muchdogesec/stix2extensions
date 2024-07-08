
from stix2 import CustomObservable
from stix2.properties import (
    ExtensionsProperty, ReferenceProperty,
    IDProperty, ListProperty, StringProperty,
    TypeProperty,
)
from ._extensions import cryptocurrency_wallet_ExtensionDefinitionSMO
_type = 'cryptocurrency-wallet'
@CustomObservable('cryptocurrency-wallet', [
    ('type', TypeProperty(_type, spec_version='2.1')),
    ('spec_version', StringProperty(fixed='2.1')),
    ('id', IDProperty(_type, spec_version='2.1')),
    ('address', StringProperty(required=True)),
    ('object_marking_refs', ListProperty(ReferenceProperty(valid_types='marking-definition', spec_version='2.1'))),
    # ('extensions', ExtensionsProperty(spec_version='2.1'))
], extension_name=cryptocurrency_wallet_ExtensionDefinitionSMO.id,id_contrib_props=['address'])
class CryptocurrencyWallet(object):
    pass

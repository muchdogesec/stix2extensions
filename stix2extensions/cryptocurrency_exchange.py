
from stix2 import CustomObservable
from stix2.properties import (
    ExtensionsProperty, ReferenceProperty,
    IDProperty, ListProperty, StringProperty,
    TimestampProperty, TypeProperty, DictionaryProperty
)
from ._extensions import cryptocurrency_exchange_ExtensionDefinitionSMO

_type = 'cryptocurrency-exchange'
@CustomObservable('cryptocurrency-exchange', [
    ('type', TypeProperty(_type, spec_version='2.1')),
    ('spec_version', StringProperty(fixed='2.1')),
    ('id', IDProperty(_type, spec_version='2.1')),
    ('name', StringProperty(required=True)),
    ('domain', StringProperty()),
    # ('extensions', ExtensionsProperty(spec_version='2.1'))
], extension_name=cryptocurrency_exchange_ExtensionDefinitionSMO.id, id_contrib_props=['domain'])
class CryptocurrencyExchange(object):
    pass

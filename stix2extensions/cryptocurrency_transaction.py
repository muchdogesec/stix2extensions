
from stix2 import CustomObservable
from stix2.properties import (
    ExtensionsProperty, ReferenceProperty,
    IDProperty, ListProperty, StringProperty,
    TimestampProperty, TypeProperty, DictionaryProperty
)
from ._extensions import cryptocurrency_transaction_ExtensionDefinitionSMO

_type = 'cryptocurrency-transaction'
@CustomObservable('cryptocurrency-transaction', [
    ('type', TypeProperty(_type, spec_version='2.1')),
    ('spec_version', StringProperty(fixed='2.1')),
    ('id', IDProperty(_type, spec_version='2.1')),
    ('symbol', StringProperty(required=True)),
    ('hash', StringProperty(required=True)),
    ('block_id', StringProperty()),
    ('fee', StringProperty()),
    ('execution_time', TimestampProperty()),
    ('input', ListProperty(DictionaryProperty())),
    ('output', ListProperty(DictionaryProperty())),
    ('object_marking_refs', ListProperty(ReferenceProperty(valid_types='marking-definition', spec_version='2.1'))),
    # ('extensions', ExtensionsProperty(spec_version='2.1'))
], extension_name=cryptocurrency_transaction_ExtensionDefinitionSMO.id, id_contrib_props=['hash', 'symbol'])
class CryptocurrencyTransaction(object):
    pass

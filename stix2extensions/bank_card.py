
from stix2 import CustomObservable
from stix2.properties import (
    ExtensionsProperty, ReferenceProperty,
    IDProperty, ListProperty, StringProperty, BooleanProperty,
    TypeProperty
)
from ._extensions import bank_card_ExtensionDefinitionSMO

_type = 'bank-card'
@CustomObservable('bank-card', [
    ('type', TypeProperty(_type, spec_version='2.1')),
    ('spec_version', StringProperty(fixed='2.1')),
    ('id', IDProperty(_type, spec_version='2.1')),
    ('format', StringProperty()),
    ('number', StringProperty(required=True)),
    ('scheme', StringProperty()),
    ('brand', StringProperty()),
    ('currency', StringProperty()),
    ('issuer_ref', ReferenceProperty(valid_types='identity', spec_version='2.1')),
    ('holder_ref', ReferenceProperty(valid_types='identity', spec_version='2.1')),
    ('valid_from', StringProperty()),
    ('valid_to', StringProperty()),
    ('security_code', StringProperty()),
    ('level', StringProperty()),
    ('is_commercial', BooleanProperty()),
    ('is_prepaid', BooleanProperty()),
    # ('extensions', ExtensionsProperty(spec_version='2.1'))
], extension_name=bank_card_ExtensionDefinitionSMO.id, id_contrib_props=['number'])
class BankCard(object):
    pass
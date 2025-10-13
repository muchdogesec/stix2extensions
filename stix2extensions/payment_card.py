
from stix2 import CustomObservable
from stix2.properties import (
    ExtensionsProperty, ReferenceProperty,
    IDProperty, ListProperty, StringProperty, BooleanProperty, TimestampProperty,
    TypeProperty
)
from ._extensions import payment_card_ExtensionDefinitionSMO

_type = 'payment-card'
@CustomObservable(_type, [
    ('type', TypeProperty(_type, spec_version='2.1')),
    ('spec_version', StringProperty(fixed='2.1')),
    ('id', IDProperty(_type, spec_version='2.1')),
    ('format', StringProperty()),
    ('value', StringProperty(required=True)),
    ('scheme', StringProperty()),
    ('brand', StringProperty()),
    ('currency', StringProperty()),
    ('issuer_ref', ReferenceProperty(valid_types='identity', spec_version='2.1')),
    ('holder_ref', ReferenceProperty(valid_types='identity', spec_version='2.1')),
    ('start_date', TimestampProperty()),
    ('expiration_date', TimestampProperty()),
    ('security_code', StringProperty()),
    ('level', StringProperty()),
    ('is_commercial', BooleanProperty()),
    ('is_prepaid', BooleanProperty()),
    # ('extensions', ExtensionsProperty(spec_version='2.1'))
], extension_name=payment_card_ExtensionDefinitionSMO.id, id_contrib_props=['value'])
class PaymentCard(object):
    pass
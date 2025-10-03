from stix2 import CustomObservable
from stix2.properties import (
    ExtensionsProperty, ReferenceProperty,
    IDProperty, ListProperty, StringProperty, BooleanProperty,
    TypeProperty
)
from ._extensions import data_source_ExtensionDefinitionSMO

_type = 'data-source'
@CustomObservable('data-source', [
    ('type', TypeProperty(_type, spec_version='2.1')),
    ('spec_version', StringProperty(fixed='2.1')),
    ('id', IDProperty(_type, spec_version='2.1')),
    ('name', StringProperty(required=True)),
    ('category', StringProperty()),
    ('product', StringProperty()),
    ('service', StringProperty()),
    ('definition', StringProperty()),
    # ('extensions', ExtensionsProperty(spec_version='2.1'))
], extension_name=data_source_ExtensionDefinitionSMO.id, id_contrib_props=['name'])
class DataSource(object):
    pass

from stix2 import CustomObject
from stix2.properties import (
    ExtensionsProperty, ReferenceProperty,
    IDProperty, ListProperty, StringProperty,
    TypeProperty,
)

from ._extensions import attack_flow_ExtensionDefinitionSMO


_type = 'attack-flow'
@CustomObject(_type, [
    ('type', TypeProperty(_type, spec_version='2.1')),
    ('spec_version', StringProperty(fixed='2.1')),
    ('id', IDProperty(_type, spec_version='2.1')),
    ('name', StringProperty(required=True)),
    ('description', StringProperty()),
    ('scope', StringProperty(required=True)),
    ('start_refs', ListProperty(ReferenceProperty(valid_types=['attack-action']))),
    
], extension_name=attack_flow_ExtensionDefinitionSMO.id)
class AttackFlow(object):
    pass


_type = 'attack-action'
@CustomObject(_type, [
    ('type', TypeProperty(_type, spec_version='2.1')),
    ('spec_version', StringProperty(fixed='2.1')),
    ('id', IDProperty(_type, spec_version='2.1')),
    ('technique_id', StringProperty(required=True)),
    ('technique_ref', ReferenceProperty(required=True, valid_types=['attack-pattern', 'x-mitre-tactic'])),
    ('tactic_id', StringProperty(required=True)),
    ('tactic_ref', ReferenceProperty(required=True, valid_types=['x-mitre-tactic'])),
    ('name', StringProperty(required=True)),
    ('effect_refs',  ListProperty(ReferenceProperty(valid_types=['attack-action']))),
])
class AttackAction(object):
    with_extension = AttackFlow.with_extension

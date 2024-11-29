import uuid
import hashlib
import stix2
import os
import json
import sys  # Missing import added here

from stix2 import Bundle
from stix2.base import STIXJSONEncoder
from uuid import UUID

from stix2extensions._extensions import (
    weakness_ExtensionDefinitionSMO,
    bank_account_ExtensionDefinitionSMO,
    bank_card_ExtensionDefinitionSMO,
    cryptocurrency_transaction_ExtensionDefinitionSMO,
    cryptocurrency_wallet_ExtensionDefinitionSMO,
    phone_number_ExtensionDefinitionSMO,
    user_agent_ExtensionDefinitionSMO,
    vulnerability_scoring_ExtensionDefinitionSMO,
    indicator_vulnerable_cpes_ExtensionDefinitionSMO,
    report_epss_scoring_ExtensionDefinitionSMO,
    software_cpe_properties_ExtensionDefinitionSMO
)

sys.path.append('generators')  # sys is now imported, so this works

from utils import Generator

# Namespace UUID for generating UUIDv5
namespace = UUID("00abedb4-aa42-466c-9c01-fed23315a9b7")

# Create and save the objects using the Generator
if __name__ == '__main__':
    generator_sdos = Generator("extension-definitions/sdos")
    generator_sdos.add_item("weakness", weakness_ExtensionDefinitionSMO)
    
    generator_scos = Generator("extension-definitions/scos")
    generator_scos.add_item("bank-account", bank_account_ExtensionDefinitionSMO)
    generator_scos.add_item("bank-card", bank_card_ExtensionDefinitionSMO)
    generator_scos.add_item("cryptocurrency-transaction", cryptocurrency_transaction_ExtensionDefinitionSMO)
    generator_scos.add_item("cryptocurrency-wallet", cryptocurrency_wallet_ExtensionDefinitionSMO)
    generator_scos.add_item("phone-number", phone_number_ExtensionDefinitionSMO)
    generator_scos.add_item("user-agent", user_agent_ExtensionDefinitionSMO)
    
    generator_properties = Generator("extension-definitions/properties")
    generator_properties.add_item("vulnerability-scoring", vulnerability_scoring_ExtensionDefinitionSMO)
    generator_properties.add_item("indicator-vulnerable-cpes", indicator_vulnerable_cpes_ExtensionDefinitionSMO)
    generator_properties.add_item("report-epss-scoring", report_epss_scoring_ExtensionDefinitionSMO)
    generator_properties.add_item("software-cpe-properties", software_cpe_properties_ExtensionDefinitionSMO)

    # Save all items
    generator_sdos.save_all()
    generator_scos.save_all()
    generator_properties.save_all()

    # Combine all objects from all generators into one bundle
    all_objects = list(generator_sdos.items.values()) + list(generator_scos.items.values()) + list(generator_properties.items.values())

    # Sort the objects by their ID to ensure consistent order
    all_objects = sorted(all_objects, key=lambda x: x['id'])

    # Create the STIX bundle
    bundle_of_all_objects = {
        "type": "bundle",
        "objects": all_objects
    }

    # Serialize the objects for MD5 hash calculation (sort_keys ensures consistency)
    bundle_objects_json_str = json.dumps(bundle_of_all_objects['objects'], cls=STIXJSONEncoder, sort_keys=True)

    # Generate the MD5 hash of the objects
    md5_hash = hashlib.md5(bundle_objects_json_str.encode('utf-8')).hexdigest()

    # Generate UUIDv5 for the bundle using the namespace and MD5 hash
    bundle_id = "bundle--" + str(uuid.uuid5(namespace, md5_hash))

    # Create the final bundle with the calculated ID
    final_bundle = Bundle(id=bundle_id, objects=all_objects, allow_custom=True)

    # Save the bundle to a file
    with open("extension-definitions/extension-definition-bundle.json", "w") as bundle_file:
        json.dump(final_bundle, bundle_file, cls=STIXJSONEncoder, indent=4)

    # Print the serialized bundle
    print(final_bundle.serialize(pretty=True))

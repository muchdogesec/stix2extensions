from stix2extensions._extensions import (
    weakness_ExtensionDefinitionSMO,
    bank_account_ExtensionDefinitionSMO,
    bank_card_ExtensionDefinitionSMO,
    cryptocurrency_transaction_ExtensionDefinitionSMO,
    cryptocurrency_wallet_ExtensionDefinitionSMO,
    cryptocurrency_exchange_ExtensionDefinitionSMO,
    phone_number_ExtensionDefinitionSMO,
    user_agent_ExtensionDefinitionSMO,
    Bundle,
    namespace
    )
import uuid
from stix2 import Bundle

if __name__ == '__main__':
        
    from utils import Generator
    generator_sdos = Generator("extension-definitions/sdos")
    generator_sdos.add_item("weakness", weakness_ExtensionDefinitionSMO)
    generator_scos = Generator("extension-definitions/scos")
    generator_scos.add_item("bank-account", bank_account_ExtensionDefinitionSMO)
    generator_scos.add_item("bank-card", bank_card_ExtensionDefinitionSMO)
    generator_scos.add_item("cryptocurrency-transaction", cryptocurrency_transaction_ExtensionDefinitionSMO)
    generator_scos.add_item("cryptocurrency-wallet", cryptocurrency_wallet_ExtensionDefinitionSMO)
    generator_scos.add_item("cryptocurrency-exchange", cryptocurrency_exchange_ExtensionDefinitionSMO)
    generator_scos.add_item("phone-number", phone_number_ExtensionDefinitionSMO)
    generator_scos.add_item("user-agent", user_agent_ExtensionDefinitionSMO)
    # generator.add_item("YOUR-NEW-OBJECT", YOUR_NEW_OBJECT_ExtensionDefinitionSMO)
    
    # Save all items for both generators
    generator_sdos.save_all()
    generator_scos.save_all()

    BundleofAllObjects = Bundle(
                            id="bundle--" + str(uuid.uuid5(namespace, f"extension-definition-bundle")), # bundle--026bf1fc-bd8b-5556-a061-14ebe3e9b8de
                            objects=list(generator_sdos.items.values()) + list(generator_scos.items.values()),
                            allow_custom=True
                        )

    ## Print the bundle

    print(BundleofAllObjects.serialize(pretty=True))
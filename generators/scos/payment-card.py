import uuid
import stix2
import os
import shutil

from uuid import UUID
from stix2extensions.payment_card import PaymentCard
# create the directories

tmp_directories = [
    "tmp_object_store",
]

for directory in tmp_directories:
    if not os.path.exists(directory):
        os.makedirs(directory)

# define UUID for generating UUIDv5s -- this is the OASIS namespace for SCOs https://github.com/oasis-open/cti-python-stix2/blob/master/stix2/base.py#L29

namespace=UUID("00abedb4-aa42-466c-9c01-fed23315a9b7")

# Create payment-card SCO

example_paymentCardSCO = PaymentCard(
                    id="payment-card--"+ str(uuid.uuid5(namespace, f"4242424242424242")), # payment-card--9ce64b19-095d-5187-a56b-79a82ae4066f
                    format="credit",
                    value="4242424242424242",
                    scheme="VISA",
                    brand="VISA",
                    currency="GBP",
                    issuer_ref="identity--9bef1584-289b-41fe-81b4-a5d72b7746d6",
                    holder_ref="identity--9fcd0db9-8115-4e33-ae00-674806395cf1",
                    start_date="1999-01-01T00:00:00Z",
                    expiration_date="2000-01-02T23:59:59Z",
                    security_code="999",
                    level="CLASSIC",
                    is_commercial=False,
                    is_prepaid=False
                    )

# Write the objects to the filestore
## https://stix2.readthedocs.io/en/latest/guide/filesystem.html#FileSystemSource

### Creating FileSystemStore and adding MarkingDefinitionSMO for each directory

fs_directories = {
    "tmp_object_store": example_paymentCardSCO
}

for directory, paymentcard_sco in fs_directories.items():
    fs_store = stix2.FileSystemStore(directory)
    fs_store.add([paymentcard_sco])

# Now move those files into the standardised locations for easy download

final_directories = [
    "example_objects/scos"
]

for directory in final_directories:
    if not os.path.exists(directory):
        os.makedirs(directory)

shutil.move("tmp_object_store/payment-card/payment-card--" + str(uuid.uuid5(namespace, f"4242424242424242")) + ".json", "example_objects/scos/payment-card--" + str(uuid.uuid5(namespace, f"4242424242424242")) + ".json")

shutil.rmtree("tmp_object_store")
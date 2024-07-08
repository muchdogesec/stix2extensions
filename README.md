# stix2extensions

## Overview

This repository is used to share custom STIX objects created by the threat intelligence community.

It is useful for two use-cases, for those who want to:

1. create their own custom STIX objects and make them easy to distribute
2. easily use the custom STIX objects created by others in this repo 

This repository currently offers the following custom STIX objects:

### SDOs

* `weakness`: This extension creates a new SDO that can be used to represent weaknesses (for CWEs).

### SCOs

* `bank-account`: This extension creates a new SCO that can be used to represent bank account details.
* `bank-card`: This extension creates a new SCO that can be used to represent bank cards.
* `cryptocurrency-transaction`: This extension creates a new SCO that can be used to represent cryptocurrency transactions.
* `cryptocurrency-wallet`: This extension creates a new SCO that can be used to represent cryptocurrency wallets.
* `phone-number`: This extension creates a new SCO that can be used to represent phone numbers.
* `user-agent`: This extension creates a new SCO that can be used to represent user agents used in HTTP request. It is designed to be used when the Network Traffic SCO with HTTP request extension cannot be used due to lack of request information needed for the required properties.

## Adding your own custom STIX objects to this repo

### Overview

First clone this repo, and set it up:

```shell
# clone the latest code
git clone https://github.com/muchdogesec/stix2extensions
# create a venv
cd stix2extensions
python3 -m venv stix2extensions-venv
source stix2extensions-venv/bin/activate
# install requirements
pip3 install .
```

To add your own objects to this repo you must then do two things:

1. define a schema for it in the `schemas` directory
2. create an entry for it in `stix2extensions` defining the properties
3. add an entry in `generators/extension-definition.py` to auto generate the Extension Definition for your objects
4. add an entry under `generators/custom-objects` for your custom object. This script should generate a dummy object to show others what it looks like

For each of these steps, you can see examples of the existing objects which you can use as a template.

### Generating the data

This script will generated the Extension Definition objects defining all of the custom objects in this repo (inc. any you've added at step 3);

```shell
python3 generators/extension-definition.py
```

If you want to see example of how to use this script to generate the custom objects (and what they look like), you can run the generator scripts (created at step 4, don't forget to add yours to the list);

```shell
python3 generators/custom-objects/weakness.py && \
python3 generators/custom-objects/bank-account.py && \
python3 generators/custom-objects/bank-card.py && \
python3 generators/custom-objects/cryptocurrency-transaction.py && \
python3 generators/custom-objects/cryptocurrency-wallet.py && \
python3 generators/custom-objects/phone-number.py && \
python3 generators/custom-objects/user-agent.py
```

#### A note about UUIDs in `generators`

Note, all of the SDO `id`s in this repo are generated by the namespace `1abb62b9-e513-5f55-8e73-8f6d7b55c237`. This is a randomly generated UUIDv4. It is used to ensure the objects generated by the code in this repo have persistent UUIDs on each update.

For all SCO object generation scripts we use the OASIS namespace `00abedb4-aa42-466c-9c01-fed23315a9b7`.

### Misc

Note, this repository also contains two scripts under `stix2extensions/tools`; 1) `creditcard2stix.py`, and 2) `crypto2stix.py`. These are utilities we use in our products.

You should use the core repositories for this data [creditcard2stix](https://github.com/muchdogesec/creditcard2stix) and [crypto2stix](https://github.com/muchdogesec/crypto2stix) respectively.

## Using the STIX objects defined in this repo

If you want to generate a custom STIX object found in this repo in your project (e.g. use the `cryptocurrency-transaction` objects to model crypto transactions) you can import them like so:

```shell
pip3 install https://github.com/muchdogesec/stix2extensions/archive/main.zip
```

You can then easily use them in your code.

For example, generate a `bank-account`;

```python
from stix2extensions import BankCard

# define UUID for generating UUIDv5s -- this is the OASIS namespace for SCOs https://github.com/oasis-open/cti-python-stix2/blob/master/stix2/base.py#L29

namespace=UUID("00abedb4-aa42-466c-9c01-fed23315a9b7")

# Create bank-card SCO

example_bankCardSCO = BankCard(
                    id="bank-card--"+ str(uuid.uuid5(namespace, f"4242424242424242")), # bank-card--9ce64b19-095d-5187-a56b-79a82ae4066f
                    format="credit",
                    number="4242424242424242",
                    scheme="VISA",
                    brand="VISA",
                    currency="GBP",
                    issuer_name="Big Bank",
                    issuer_country="GBR",
                    holder_name="DOGESEC",
                    valid_from="01/99",
                    valid_to="01/00",
                    security_code="999"
                    )

print(example_bankCardSCO)
```

## Support

[Minimal support provided via the DOGESEC community](https://community.dogesec.com).

## License

[Apache 2.0](/LICENSE).

## Useful supporting tools

* Existing STIX 2.1 schemas: [cti-stix2-json-schemas](https://github.com/oasis-open/cti-stix2-json-schemas): OASIS TC Open Repository: Non-normative schemas and examples for STIX 2
* To generate STIX 2.1 extensions: [stix2 Python Lib](https://stix2.readthedocs.io/en/latest/)
* STIX 2.1 specifications for objects: [STIX 2.1 docs](https://docs.oasis-open.org/cti/stix/v2.1/stix-v2.1.html)
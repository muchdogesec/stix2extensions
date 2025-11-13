# stix2extensions

## Overview

This repository is used to share custom STIX objects and STIX object extensions created by the threat intelligence community.

It is useful for two use-cases, for those who want to:

1. create their own custom STIX objects and make them easy to distribute
2. use the custom STIX objects created by others in a straight-forward way

## Submitting your own STIX Extension Definition

To submit your own STIX Extension Definition:

1. follow the logic described in `docs/create_new_extension`
2. submit a PR to this repository for review

Once your object has been accepted, it will then be easily importable...

## Using custom object or properties defined in STIX Extension Definition

If you want to generate a custom STIX object found in this repo in your project (e.g. use the `bank-accont` STIX object to model bank accounts in your research) you can install the package and import it directly into your project.

```shell
pip3 install stix2extensions
```

You can then import and instantiate the `BankAccount` object like this:

```python
from stix2extensions import BankAccount

example_bank_account = BankAccount(
                    bank="Big Bank",
                    country="GBR",
                    currency="GBP",
                    holder_ref="identity--fb76b7b8-8701-5d8b-a143-0283847f6638",
                    iban="GB33BUKB20201555555555",
                    bic="DEMOGB22XXX",
                    )

print(example_bank_account)
```

Which prints the STIX object.

```json
{
    "type": "bank-account",
    "spec_version": "2.1",
    "id": "bank-account--a7348a10-f1b6-5b3d-8908-0ca0f67a5fb5",
    "country": "GBR",
    "currency": "GBP",
    "bank": "Big Bank",
    "holder_ref": "identity--fb76b7b8-8701-5d8b-a143-0283847f6638",
    "iban": "GB33BUKB20201555555555",
    "bic": "DEMOGB22XXX",
    "extensions": {
        "extension-definition--f19f3291-6a84-5674-b311-d75a925d5bd9": {
            "extension_type": "new-sco"
        }
    }
}
```

### Misc

Note, this repository also contains two scripts under `stix2extensions/tools`; 1) `creditcard2stix.py`, and 2) `crypto2stix.py`. These are utilities we use in our products to generate enrichments to the `cryptocurrency-wallet`, `cryptocurrency-transaction`, and `bank-card` objects.

## Support

[Minimal support provided via the DOGESEC community](https://community.dogesec.com).

## License

[Apache 2.0](/LICENSE).

## Useful supporting tools

* Existing STIX 2.1 schemas: [cti-stix2-json-schemas](https://github.com/oasis-open/cti-stix2-json-schemas): OASIS TC Open Repository: Non-normative schemas and examples for STIX 2
* To generate STIX 2.1 extensions: [stix2 Python Lib](https://stix2.readthedocs.io/en/latest/)
* STIX 2.1 specifications for objects: [STIX 2.1 docs](https://docs.oasis-open.org/cti/stix/v2.1/stix-v2.1.html)
* [stix2icons](https://github.com/muchdogesec/stix2icons): icons for the custom STIX objects in this repository
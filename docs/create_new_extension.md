# Create a new Extension Definition

This guide walks you through everything you need to create a new STIX Extension.

stix2extensions will allow you to;

1. Create a new SDO, or
2. Create a new SCO, or
3. Add new properties to an existing SDO or SCO

---

## 0. Set up 

### 0.1 Install the requirements

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

### 0.2 Understand the directory structure

In `definitions/` you will find the following directories that contain the definitions (Python files used to generate all assets) based on each of the available extension creation options;

```
definitions/
├── sdos/
├── scos/
└── properties/
```

---

## 1. Create a new SDO

### 1.1 Create a skeleton file

You should add a new file in `definitions/sdos` and name it in the structure `<OBJECT TYPE (SNAKE CASE).py`.

For example, `nation-state` would use the file name `definitions/sdos/nation_state.py`

### 1.2 Define imports

Thus all depends on the structure of you object.

```python
from datetime import UTC, datetime
from enum import StrEnum

from stix2 import CustomObject

from stix2.properties import (
    ListProperty,
    StringProperty,
    OpenVocabProperty,
    EnumProperty,
)

from stix2extensions.automodel import ExtensionType, automodel, extend_property
```

Let me try and break this down...

```python
from datetime import UTC, datetime
```

Used to generate Extension Definition `created` and `modified` times in expected format (see 1.4).

```python
from enum import StrEnum
```

Optional. Only required where `EnumProperty` is used in the object. See `weakness.py` for a good example.

**A small note on imports**: You can use other libraries to support the generation of data for the schema examples. `enum` and `datetime` are just two examples for this documentation.

```python
from stix2 import CustomObject
```

This line is always required for SDOs. Defines that it is an SDO type object.

```python
from stix2.properties import (
    ListProperty,
    StringProperty,
    OpenVocabProperty,
    EnumProperty,
)
```

This depends on the datatypes you will use for the values inside your object.

[The available options are defined in the stix2 library here](https://stix2.readthedocs.io/en/latest/api/stix2.properties.html?highlight=listproperty)

```python
from stix2extensions.automodel import ExtensionType, automodel, extend_property
```

Always required to import the scaffolding to generate the output.

### 1.3 Define the object structure

Here is a demo `nation_state.py` that I will use to show the basics of modelling an object in your definition file;

```python
_type = "nation-state"

@automodel
@CustomObject(
    _type,
    [
        (
            "name",
            extend_property(
                StringProperty(required=True),
                description="The name of the Nation State",
                examples=["Russian Federation", "The Democratic People's Republic of Korea"],
            ),
        ),
        (
            "description",
            extend_property(
                StringProperty(),
                description="Detailed description of the Nation State",
                examples=[
                    "North Korea’s (DPRK) cyber activities are among the most aggressive and well-organized state-sponsored operations globally, blending espionage, financial crime, and disruptive attacks to advance regime objectives."
                ],
            ),
        ),
        (
            "location_ref",
            extend_property(
                ReferenceProperty(valid_types="location", spec_version="2.1"),
                description="STIX location object representing the political captial of the Nation State",
                examples=["location--d5c93aa7-eaa5-5dc8-8dfa-c15f1f51fbaa"],
            ),
        )
    ]
)
```

**What each piece does:**

* `_type = "nation-state"`: defines the object type 
* `@automodel`: Adds the usual model “plumbing” (constructor, validation, etc.) so you can instantiate the object like a normal Python class.
* `@CustomObject(_type, [...])`: Registers a new STIX object (SDO) type with the name `weakness`.
	* The first argument (`_type`) calls the type
	* The second argument is a list of property definitions...

Each property is a tuple of:

```python
("<property_name>", <property_definition>)
```

For example:

```python
        (
            "name",
            extend_property(
                StringProperty(required=True),
                description="The name of the Nation State",
                examples=["Russian Federation", "The Democratic People's Republic of Korea"],
            ),
        ),
```

* `name`: the property name.
* `StringProperty(required=True)`: the data type and requirements. [You can get a full list of data types available to use here](https://stix2.readthedocs.io/en/latest/api/stix2.properties.html). Remember to import them properly (see 1.2).
* `description`: a clear description of this property that is used in generated docs / schema.
* `examples`: example value(s) for this property that are used in generated docs / schema.

You must always pass these four values for each property you are defining.

This is a very simple example of defining the object structure. See the other existing objects for examples of what can be done.

### 1.4 Define the class

Inside your custom STIX object class, you sjpi;d define metadata about the extension itself — such as its purpose and last modification date.

```python
class NationState(ExtensionType):
    extension_description = "This extension creates a new SDO to represent Nation States."
    extension_created = datetime(2020, 1, 1, tzinfo=UTC)
    extension_modified = datetime(2025, 11, 5, tzinfo=UTC)
    extension_version = "1.1"
```

* `extension_description` [REQUIRED]: (string) will be used in the Extension Definition objects `description` and for the `description` of the schema
* `extension_created` [OPTIONAL, defaults to `2020-01-01` if not set]: (datetime) will be used as the `created` date of the Extension Definition. Do not change this (or add it later) once your first version is published.
* `extension_modified` [defaults to `extension_created` if not set, ALWAYS set to current date when modifying published Extension]: (datetime) will be used as the `modified` date of the Extension Definition.
* `extension_version` [OPTIONAL, defaults to `1.0` if not set]: (string) Will be used as the `version` property of the extension definition.

### 1.5 Generate the extension assets

You can not run the script to generate your 

```shell
python generate_all.py
```

---

## 2. Create a new SCO

### 2.1 Create a skeleton file

You should add a new file in `definitions/scos` and name it in the structure `<OBJECT TYPE (SNAKE CASE).py`.

For example, `my-new-sco` would use the file name `definitions/scos/my_new_sco.py`

### 2.2 Define imports

First read 1.2.

The only difference being you should always use `from stix2 import CustomObservable` NOT `from stix2 import CustomObject` to declare that this is an SCO type object.

### 2.3 Define the object structure

First read 2.3.

There are two important differences: 

1. always use `@CustomObservable(` NOT `@CustomObject(` because this will be an SCO.
2. add `id_contrib_props=["PROPERTY"],`: SDO IDs use random UUIDv4s. SCOs use UUIDv5s. You must specify one or more properties that will be used to generate the UUID. These should be atomic, stable values—for example, an IP address object should use the IP address string itself. This guarantees that the same real-world object (e.g., the same IP) always results in the same STIX ID.

#### A note about UUIDv5s

For all SCO object generation scripts the OASIS namespace `00abedb4-aa42-466c-9c01-fed23315a9b7` will be used (as because generation is done by the stix2 Python library where this namespace is used).

### 2.4 Define the class

First read 1.4.

Compared to generating SDOs, there is one difference I will highlight these by showing SDO option -> SCO change required

* add `at_least_one_of` defining a list of properties where at least one must exist. Generally this should match the list of `id_contrib_props` defined at 2.3.

### 2.5 Generate the extension assets

See 1.5.

---

## 3. Add new properties to an existing SDO or SCO

### 3.1 Create a skeleton file

You should add a new file in `definitions/properties` and name it in the structure `<OBJECT TYPE EXTENDED>_<SHORT IDENTIFIER>(SNAKE CASE).py`.

For example, if you were extending an Identity objects to include new alias fields you might name it `identity_extended_aliases.py`. 

Generally the `<SHORT IDENTIFIER>` can be anything, but it MUST result in a unique filename.

### 3.2 Define imports

Compared to 1.2 (SDO) and 2.2 (SCO) the imports are slightly different here.

There is no need to import `CustomObservable` or `CustomObject` from stix2. Instead, you need to import from stix2extensions the following

```python
from stix2extensions.automodel.property_extension import (
    CustomPropertyExtension,
    ExtensionTypes,
)
```

In the examples you will also see

```python
from typing import OrderedDict
```

Whilst this is optional, it is recommended so you can define the order the properties appear (see. 3.3)

### 3.3 Define the object structure

Here is a basic example defining new properties for my identity object

```python
@automodel
@CustomPropertyExtension(
    extension_id="identity-extended-aliases",
    properties=OrderedDict(
        [
            (
                "aliases",
                extend_property(
                    StringProperty(),
                    description="Aliases this identity goes by",
                    examples=["CompanyX"],
                ),
            ),
            (
                "nicknames",
                extend_property(
                    StringProperty(),
                    description="Nicknames for this identity",
                    examples=["X"],
                ),
            ),
        ]
    ),
    extension_type=ExtensionTypes.TOPLEVEL_PROPERTY_EXTENSION,
)
```

The structure here is slightly different to 1.4 and 2.4...

* `@CustomPropertyExtension`: Registers a new the new properties
    * The first argument (`extension_id`) defines the name of the extension. This will be used to generate schema file name and the UUID of the Extension Definition object
    * The second argument (`properties=OrderedDict`) is contains a list of the new properties you wish to add. We use `OrderedDict` to ensure the properties appear in this order. This is optional, but if used be sure to import it (see 3.2)
    * The third argument (`extension_type`) defines what type of extension you want to use. Currently stix2extension only supports `toplevel-property-extension` so you must always use `ExtensionTypes.TOPLEVEL_PROPERTY_EXTENSION`.[Consult the STIX specification (Extension Types Enumeration) if you are unsure if this is right for you](https://docs.oasis-open.org/cti/stix/v2.1/cs02/stix-v2.1-cs02.html#_f23s79k9bdhl)

### 3.4 Define the class

Again, similar to 1.4 but the this time also required you to pass `base_schema_ref`, e.g.

```python
class IndicatorVulnerableCPEPropertyExtension(ExtensionType):
    base_schema_ref = "https://raw.githubusercontent.com/oasis-open/cti-stix2-json-schemas/master/schemas/sdos/indicator.json"
    extension_description = "This extension adds new properties to Indicator SDOs to list CPE vulnerable inside a pattern."
    extension_created = datetime(2020, 1, 1, tzinfo=UTC)
    extension_modified = datetime(2025, 11, 5, tzinfo=UTC)
    extension_version = "1.0"
```

* `base_schema_ref`: points to the schema of the object you are extending. Generally speaking you can find these schemas here:
    * [for Core STIX SDOs](https://github.com/oasis-open/cti-stix2-json-schemas/tree/master/schemas/sdos)
    * [for Core STIX SCOs](https://github.com/oasis-open/cti-stix2-json-schemas/tree/master/schemas/observables)

**IMPORTANT**: We recommend only extending the Core STIX objects in this way. For Custom STIX objects defined in this repo it is usually always better to modify the Custom object itself and submit a PR to have it improved.

### 3.5 Generate the extension assets

See 1.5.
# Create a new Extension Definition

This guide walks you through everything you need to create a new STIX Extension.

## 0. Create a skeleton definition file

Before starting you need to decide if you wish to create:

1. A new SDO
2. A new SCO
3. new properties for an SDO/SCO

In `definitions/` you will find the following directories that contain the definitions based on each of these options;

```
definitions/
├── sdos/
├── scos/
└── properties/
```

## 1. Create a new SDO

### 1.1 Create a skeleton file

You should add a new file in either `definitions/sdos` and name it in the structure `<OBJECT TYPE (SNAKE CASE).py`.

For example, `my-new-sdo` would use the file name `definitions/sdos/my_new_sdo.py`

### 1.2 Define imports

TODO: https://github.com/muchdogesec/stix2extensions/issues/69

### 1.3 Define the object structure

At this point it is best to consult the examples the already exist in `definitions/sdos/`

Here is a snippet from `weakness.py`;

```python
@automodel
@CustomObject(
    "weakness",
    [
        (
            "name",
            extend_property(
                StringProperty(required=True),
                description="Name of the weakness as defined in CWE",
                examples=["Buffer Overflow", "SQL Injection"],
            ),
        ),
        (
            "description",
            extend_property(
                StringProperty(),
                description="Detailed description of the weakness",
                examples=[
                    "A buffer overflow occurs when data exceeds the allocated buffer memory, potentially allowing code execution."
                ],
            ),
        ),
        (
            "likelihood_of_exploit",
            extend_property(
                EnumProperty(allowed=["High", "Medium", "Low"]),
                description="Likelihood that the weakness can be successfully exploited",
            ),
        ),
        (
            "common_consequences",
            extend_property(
                ListProperty(
                    extend_property(
                        OpenVocabProperty(allowed=COMMON_CONSEQUENCES_OV),
                        description="Typical impact categories resulting from exploitation of this weakness.",
                    )
                ),
                description="Typical impacts or consequences resulting from the weakness",
            ),
        )
    ]
)
```

**What each piece does:**

* `@automodel`: Adds the usual model “plumbing” (constructor, validation, etc.) so you can instantiate the object like a normal Python class.
* `@CustomObject("weakness", [...])`: Registers a new STIX object type with the name `weakness`.
	* The first argument (`weakness`) is the STIX type name (what will appear in the type field of the object) and should match the filename.
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
        description="Name of the weakness as defined in CWE",
        examples=["Buffer Overflow", "SQL Injection"],
    ),
)
```

* `name`: the property name.
* `StringProperty(required=True)`: the data type and requirements.
* `description`: a clear description of this property that is used in generated docs / schema.
* `examples`: example value(s) for this property that are used in generated docs / schema.

You must always pass these four values for each property you are defining.

[You can get a full list of data types available to use here](https://stix2.readthedocs.io/en/latest/api/stix2.properties.html). Again, to see what is possible when defining properties for your object, consult the existing objects which show a good range of examples/


### Define the class

```python
class Weakness(ExtensionType):
    description = "This extension creates a new SDO that can be used to represent weaknesses (for CWEs)."
    extension_modified = datetime(2025, 11, 5, tzinfo=UTC)
```

### If you are creating a new SDO / SCO

You should add a new file in either `definitions/sdos` or `definitions/scos` (depending on object type) and name it in the structure `<OBJECT TYPE (KEBAB CASE).py`.

For example, `bank-account` would use `definitions/scos/bank_account.py`

### If you are adding properties to an existing SDO / SCO

You should add a new file in `definitions/properties` in the format `<OBJECT TYPE BEING EXTENDED_<SHORT DESCRIPTION>.py`

For example, for Identity object extended with OpenCTI properties you could name it `identity_opencti.py`



## 2. Decide what you need to import




## 3. Define the 

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

To add your own objects to this repo you must then do the following things:

1. define a schema for it in the `schemas` directory.
2. create an entry for it in `stix2extensions` defining the properties
3. add an entry in `stix2extensions/_extensions.py` and `generators/extension-definition.py` to auto generate the Extension Definition for your objects. Then the script `python3 generators/extension-definition.py`
4. optional: add an entry under `generators/example_objects/` for your custom object. This script should generate a dummy object to show others what it looks like (this is more likely to increase adoption). Then run the script `generators/scos/*.py`.
5. optional: add an icon for your new object in our [stix2icons repository](https://github.com/muchdogesec/stix2icons). This will make it easy for graph viewers to render your object properly with an icon.




#### A note about UUIDs in `generators`

Note, all of the SDO `id`s in this repo are generated by the namespace `1abb62b9-e513-5f55-8e73-8f6d7b55c237`. This is a randomly generated UUIDv4. It is used to ensure the objects generated by the code in this repo have persistent UUIDs on each update.

For all SCO object generation scripts we use the OASIS namespace `00abedb4-aa42-466c-9c01-fed23315a9b7`.

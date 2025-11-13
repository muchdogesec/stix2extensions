import json
from pathlib import Path

from stix2extensions.automodel.automodel import AUTOMODEL_REGISTRY
from stix2 import base

import json

from stix2extensions.automodel.definitions import get_extension_type_name, get_title
# Generate Schema for all objects registered (writes to file)
base_dir = Path("automodel_generated/")
schema_dir = base_dir/'schemas'
ext_dir = base_dir/'extension-definitions'
ext_dir.mkdir(parents=True, exist_ok=True)
schema_dir.mkdir(parents=True, exist_ok=True)

for model in AUTOMODEL_REGISTRY:
    if not hasattr(model, '_type'):
        continue
    k = get_title(model)
    dir = get_extension_type_name(model)
    name = f"{dir}/{k}.json"
    path = schema_dir/name
    ext_path = ext_dir/name
    print(path, model.__name__)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(model.schema, indent=4))
    if hasattr(model, 'extension_definition'):
        ext_path.parent.mkdir(parents=True, exist_ok=True)
        ext_path.write_text(model.extension_definition.serialize(indent=4))

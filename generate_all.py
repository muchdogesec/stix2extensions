import json
from pathlib import Path

from stix2extensions.automodel.automodel import AUTOMODEL_REGISTRY

import json

# Generate Schema for all objects registered (writes to file)
base = Path("automodel_generated/")
schema_dir = base/'schemas'
ext_dir = base/'extensions'
ext_dir.mkdir(parents=True, exist_ok=True)
schema_dir.mkdir(parents=True, exist_ok=True)
for model in AUTOMODEL_REGISTRY:
    if not hasattr(model, '_type'):
        continue
    k = model._type
    path: Path = schema_dir/(k+'.json')
    ext_path: Path = ext_dir/(k+'.json')
    print(path, model.__name__)
    try:
        path.write_text(json.dumps(model.schema, indent=4))
        if hasattr(model, 'extension_definition'):
            ext_path.write_text(model.extension_definition.serialize(indent=4))
    except Exception as e:
        print(e)

import stix2
from pathlib import Path
class Generator:
    def __init__(self, path) -> None:
        self.path = Path(path)
        self.items : dict[str, stix2.observables._Observable] = dict()
        self.path.mkdir(parents=True, exist_ok=True)
        # self.type = type
    def add_item(self, name, item):
        self.items[name] = item
        # self.fs.add(item)

    def save_all(self):
        for name, item in self.items.items():
            path = self.path/f"{name}.json"
            path.write_text(item.serialize(pretty=True))
            print(f"{name} => {path}")
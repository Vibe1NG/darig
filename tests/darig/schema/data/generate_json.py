import json
from pathlib import Path

from ruamel.yaml import YAML


def generate():
    data_dir = Path("tests/darig/schema/data/")
    yaml = YAML(typ="rt")

    for yaml_path in data_dir.rglob("*.yaml"):
        try:
            with open(yaml_path) as f:
                docs = list(yaml.load_all(f))

            if not docs:
                continue

            json_path = yaml_path.with_suffix(".json")
            with open(json_path, "w") as f:
                if len(docs) == 1:
                    json.dump(docs[0], f, indent=2)
                else:
                    json.dump(docs, f, indent=2)
            print(f"Generated {json_path}")
        except Exception as e:
            print(f"Skipped {yaml_path.name}: {e}")


if __name__ == "__main__":
    generate()

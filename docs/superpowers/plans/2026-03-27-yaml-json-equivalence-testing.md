# YAML to JSON Equivalence Testing Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement automated equivalence testing for YAML and JSON data parsing in darig.schema.

**Architecture:** Create static JSON equivalents of existing YAML data test files via a one-off script, then implement a parameterized pytest module that discovers these files dynamically, loads all schemas per test, and ensures both formats yield deeply identical Pydantic models or validation failures.

**Tech Stack:** Python, `pytest`, `ruamel.yaml`, `json`, `darig.schema`.

---

### Task 1: Generate JSON counterparts for YAML data files

**Files:**
- Create: `tests/darig/schema/data/generate_json.py` (temporary script)
- Create: `tests/darig/schema/data/**/*.json` (generated)

- [ ] **Step 1: Write the generation script**

Create `tests/darig/schema/data/generate_json.py` with the following:
```python
import json
import logging
from pathlib import Path
from ruamel.yaml import YAML

log = logging.getLogger(__name__)

def generate():
    data_dir = Path(__file__).parent
    yaml = YAML(typ="rt")
    
    for yaml_path in data_dir.rglob("*.yaml"):
        try:
            with open(yaml_path) as f:
                docs = list(yaml.load_all(f))
            
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
```

- [ ] **Step 2: Run the script to generate `.json` files**

Run: `uv run python tests/darig/schema/data/generate_json.py`
Expected: Output showing generated JSON files for each YAML file.

- [ ] **Step 3: Delete the temporary script**

Run: `rm tests/darig/schema/data/generate_json.py`
Expected: File deleted.

- [ ] **Step 4: Commit the generated JSON files**

Run:
```bash
git add tests/darig/schema/data/
git commit -m "test: generate static JSON counterparts for YAML data files"
```
Expected: All newly created JSON files committed.

---

### Task 2: Implement Generic Equivalence Test

**Files:**
- Create: `tests/darig/schema/test_yaml_json_equivalence.py`

- [ ] **Step 1: Write the test logic**

Create `tests/darig/schema/test_yaml_json_equivalence.py`:
```python
import os
import pytest
from pathlib import Path
from darig.schema.core import load_data_files, load_schema_files
from darig.schema.cache import DarigSchemaRegistry

DATA_DIR = Path(__file__).parent / "data"
YAML_FILES = list(DATA_DIR.rglob("*.yaml"))

@pytest.fixture(autouse=True)
def load_all_schemas():
    """Clear registry and load all schemas before each test to prevent state leakage."""
    registry = DarigSchemaRegistry()
    registry.clear_caches()
    for yasl_file in DATA_DIR.rglob("*.yasl"):
        load_schema_files(str(yasl_file))
    yield
    registry.clear_caches()

@pytest.mark.parametrize("yaml_path", YAML_FILES, ids=lambda p: p.name)
def test_yaml_json_equivalence(yaml_path):
    json_path = yaml_path.with_suffix(".json")
    assert json_path.exists(), f"Missing JSON counterpart for {yaml_path.name}"
    
    # load_data_files catches errors and returns None on failure, or a list of Pydantic models on success.
    yaml_result = load_data_files(str(yaml_path))
    json_result = load_data_files(str(json_path))
    
    if yaml_result is None:
        assert json_result is None, f"JSON validation succeeded but YAML failed for {yaml_path.name}"
    else:
        assert json_result is not None, f"YAML validation succeeded but JSON failed for {yaml_path.name}"
        # Pydantic models and lists support deep equality checks
        assert yaml_result == json_result, f"Parsed objects mismatch for {yaml_path.name}"
```

- [ ] **Step 2: Run the test to verify equivalence**

Run: `uv run pytest tests/darig/schema/test_yaml_json_equivalence.py -v`
Expected: The test should PASS for all files. `darig.schema` should treat the static JSON identical to the YAML inputs, whether it succeeds in validation or fails.

- [ ] **Step 3: Commit the test**

Run:
```bash
git add tests/darig/schema/test_yaml_json_equivalence.py
git commit -m "test: add generic equivalence test for YAML and JSON data parsing"
```
Expected: File committed successfully.

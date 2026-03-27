# YAML to JSON Equivalence Testing Design

## Overview
The goal is to improve automated testing in `darig.schema` by ensuring that data parsing behaves identically whether the data is provided as a YAML file (`.yaml`) or a JSON file (`.json`). The design leverages static JSON replication of existing YAML data test files and introduces a discoverable equivalence test.

## 1. Data Replication (`tests/darig/schema/data/*.json`)
- For every existing `.yaml` data file in `tests/darig/schema/data/` (e.g., `forward_ref.yaml`, `presence_required_invalid.yaml`), a static JSON counterpart will be generated and committed to the repository (e.g., `forward_ref.json`, `presence_required_invalid.json`).
- These JSON files will represent the exact same data structure, providing a stable, version-controlled baseline for equivalence testing.

## 2. Generic Equivalence Test (`tests/darig/schema/test_yaml_json_equivalence.py`)
- A new `pytest` module will be created.
- The test suite will dynamically discover all `.yaml` files in the `tests/darig/schema/data/` directory.
- `pytest.mark.parametrize` will be used to generate an independent test case for each `.yaml` / `.json` file pair. This ensures that failures are tracked per file, rather than failing the entire loop.

## 3. Testing Logic (Equality and Validation)
For each parameterized test case:
- **Setup**: The `DarigSchemaRegistry` will be cleared to avoid state leakage between tests. It will then be populated with all `.yasl` schemas from the `data` directory to support schema auto-detection.
- **Execution**: `load_data_files()` from `darig.schema.core` will be called on both the `.yaml` and `.json` file paths.
- **Assertion (Valid Data)**: If validation is successful and returns populated Pydantic model(s), the test will assert deep equality between the objects (`yaml_result == json_result`).
- **Assertion (Invalid Data)**: If a data file is intended to fail validation (e.g., due to missing required fields), both the `.yaml` and `.json` files must fail identically. The test will assert that both function calls return exactly the same result (e.g., `None` or an empty list).

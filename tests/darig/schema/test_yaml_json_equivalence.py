from collections.abc import Generator
from pathlib import Path
from typing import Any

import pytest

from darig.schema.cache import DarigSchemaRegistry
from darig.schema.core import load_data_files, load_schema_files

DATA_DIR = Path(__file__).parent / "data"
YAML_FILES = list(DATA_DIR.rglob("*.yaml"))


@pytest.fixture(autouse=True)
def load_all_schemas() -> Generator[None, None, None]:
    """Clear registry and load all schemas before each test to prevent state leakage."""
    registry = DarigSchemaRegistry()
    registry.clear_caches()
    for yasl_file in DATA_DIR.rglob("*.yasl"):
        load_schema_files(str(yasl_file))
    yield
    registry.clear_caches()


@pytest.mark.parametrize("yaml_path", YAML_FILES, ids=lambda p: p.name)
def test_yaml_json_equivalence(yaml_path: Path) -> None:
    json_path = yaml_path.with_suffix(".json")
    assert json_path.exists(), f"Missing JSON counterpart for {yaml_path.name}"

    # load_data_files catches errors and returns None on failure, or a list of Pydantic models on success.
    registry = DarigSchemaRegistry()
    registry.unique_values_store.clear()

    yaml_result = load_data_files(str(yaml_path))

    registry.unique_values_store.clear()
    json_result = load_data_files(str(json_path))

    if yaml_result is None:
        assert json_result is None, (
            f"JSON validation succeeded but YAML failed for {yaml_path.name}"
        )
    else:
        assert json_result is not None, (
            f"YAML validation succeeded but JSON failed for {yaml_path.name}"
        )

        # Pydantic models and lists support deep equality checks
        # YAML parsing populates 'yaml_line' (excluded from dump) while JSON does not.
        def dump_models(result: list[Any]) -> list[dict[str, Any]]:
            return [m.model_dump() for m in result]

        assert dump_models(yaml_result) == dump_models(json_result), (
            f"Parsed objects mismatch for {yaml_path.name}"
        )

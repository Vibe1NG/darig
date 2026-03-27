import os
import tempfile

import pytest

from darig.schema.core import load_data_files, load_schema_files

SCHEMA_CONTENT = """
metadata:
  version: 1.0.0
definitions:
  test_ns:
    types:
      TestRecord:
        properties:
          id:
            type: int
          name:
            type: str
"""

JSON_CONTENT = """
{
  "id": 1,
  "name": "Test1"
}
"""

JSON_LIST_CONTENT = """
[
  {
    "id": 1,
    "name": "Test1"
  },
  {
    "id": 2,
    "name": "Test2"
  }
]
"""

JSONL_CONTENT = """
{"id": 1, "name": "Test1"}
{"id": 2, "name": "Test2"}
"""


def test_load_json_data():
    with tempfile.TemporaryDirectory() as tmpdir:
        schema_path = os.path.join(tmpdir, "test.yasl")
        json_path = os.path.join(tmpdir, "test.json")
        json_list_path = os.path.join(tmpdir, "test_list.json")
        jsonl_path = os.path.join(tmpdir, "test.jsonl")

        with open(schema_path, "w") as f:
            f.write(SCHEMA_CONTENT)
        with open(json_path, "w") as f:
            f.write(JSON_CONTENT)
        with open(json_list_path, "w") as f:
            f.write(JSON_LIST_CONTENT)
        with open(jsonl_path, "w") as f:
            f.write(JSONL_CONTENT)

        schema_res = load_schema_files(schema_path)
        assert schema_res is not None

        # Test single json
        data_res = load_data_files(json_path)
        assert data_res is not None
        assert len(data_res) == 1
        assert data_res[0].id == 1
        assert data_res[0].name == "Test1"

        # Test list json
        data_res = load_data_files(json_list_path)
        assert data_res is not None
        assert len(data_res) == 2
        assert data_res[0].id == 1
        assert data_res[1].id == 2

        # Test jsonl
        data_res = load_data_files(jsonl_path)
        assert data_res is not None
        assert len(data_res) == 2
        assert data_res[0].id == 1
        assert data_res[1].id == 2


if __name__ == "__main__":
    pytest.main([__file__])

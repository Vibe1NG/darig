import os
import subprocess
import sys
import tempfile
from io import StringIO
from pathlib import Path

import pytest
from .schema_data import (
    CUSTOMER_LIST_YASL,
    MARKDOWN_YASL,
    NAMESPACE_CUSTOMER_LIST_YASL,
    PERSON_ADDRESS_MULTI_YASL,
    PERSON_WEBSITE_REACHABLE_YAML,
    PERSON_YASL,
    PYDANTIC_TYPES_YASL,
    REF_LIST_YASL,
    SHAPE_YASL,
    TASK_BAD_NAMESPACE_REF_YASL,
    TODO_BAD_MAP_VALUE_YASL,
    TODO_BOOL_MAP_YASL,
    TODO_DOT_NAMESPACE_YASL,
    TODO_ENUM_MAP_YASL,
    TODO_INT_MAP_YASL,
    TODO_MIXED_NAMESPACE_YASL,
    TODO_NESTED_MAP_YASL,
    TODO_YASL,
)

from darig.schema import yasl_eval
from darig.cli import main as yasl_cli_main


def run_cli(args):
    filtered_args = [item for item in args if item is not None]
    result = subprocess.run(["darig"] + filtered_args, capture_output=True, text=True)
    return result


def test_cli_version(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["darig", "--version"])
    with pytest.raises(SystemExit) as e:
        yasl_cli_main()
    assert e.value.code == 0
    captured = capsys.readouterr()
    assert "Darig version" in captured.out


def test_cli_quiet_and_verbose(monkeypatch, capsys):
    monkeypatch.setattr(
        sys,
        "argv",
        ["darig", "--quiet", "--verbose", "check", "file.yasl", "data.yaml"],
    )
    with pytest.raises(SystemExit) as e:
        yasl_cli_main()
    assert e.value.code == 1
    captured = capsys.readouterr()
    assert "❌ Cannot use both --quiet and --verbose." in captured.out


def test_cli_missing_args(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["darig", "check"])
    with pytest.raises(SystemExit) as e:
        yasl_cli_main()
    assert e.value.code == 2
    captured = capsys.readouterr()
    assert "the following arguments are required" in captured.err


def test_cli_good(monkeypatch, capsys):
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "darig",
            "check",
            "./features/darig/schema/data/todo.yasl",
            "./features/darig/schema/data/todo.yaml",
            "--model",
            "list_of_tasks",
        ],
    )
    with pytest.raises(SystemExit) as e:
        yasl_cli_main()
    assert e.value.code == 0


def test_quiet_and_verbose():
    result = run_cli(["--quiet", "--verbose", "check", "file.yasl", "file.yaml"])
    assert result.returncode != 0
    assert "Cannot use both" in result.stdout


def run_eval_command(yaml_data, yasl_schema, model_name, expect_valid):
    with tempfile.TemporaryDirectory() as tmpdir:
        yaml_path = os.path.join(tmpdir, "test.yaml")
        yasl_path = os.path.join(tmpdir, "test.yasl")
        with open(yaml_path, "w") as f:
            f.write(yaml_data)
        with open(yasl_path, "w") as f:
            f.write(yasl_schema)

        args = ["--quiet", "check", yasl_path, yaml_path, "--model", model_name]
        result = run_cli(args)

        if expect_valid:
            assert result.returncode == 0, (
                f"Validation failed for {model_name}: {result.stdout}\n{result.stderr}"
            )
        else:
            assert result.returncode != 0, (
                f"Validation succeeded unexpectedly for {model_name}"
            )


def test_basic_validation():
    run_eval_command(PERSON_YASL, PERSON_YASL, "person", True)


def test_todo_list():
    run_eval_command(TODO_YASL, TODO_YASL, "list_of_tasks", True)


def test_customer_list():
    run_eval_command(CUSTOMER_LIST_YASL, CUSTOMER_LIST_YASL, "customer_list", True)


def test_shapes():
    run_eval_command(SHAPE_YASL, SHAPE_YASL, "shape", True)


def test_pydantic_types():
    run_eval_command(PYDANTIC_TYPES_YASL, PYDANTIC_TYPES_YASL, "pydantic_types", True)


def test_mixed_namespace():
    run_eval_command(
        TODO_MIXED_NAMESPACE_YASL, TODO_MIXED_NAMESPACE_YASL, "list_of_tasks", True
    )


def test_dot_namespace():
    run_eval_command(
        TODO_DOT_NAMESPACE_YASL, TODO_DOT_NAMESPACE_YASL, "list_of_tasks", True
    )


def test_int_map():
    run_eval_command(TODO_INT_MAP_YASL, TODO_INT_MAP_YASL, "list_of_tasks", True)


def test_enum_map():
    run_eval_command(TODO_ENUM_MAP_YASL, TODO_ENUM_MAP_YASL, "list_of_tasks", True)


def test_bool_map():
    run_eval_command(TODO_BOOL_MAP_YASL, TODO_BOOL_MAP_YASL, "list_of_tasks", False)


def test_nested_map():
    run_eval_command(TODO_NESTED_MAP_YASL, TODO_NESTED_MAP_YASL, "list_of_tasks", True)


def test_bad_map_value():
    run_eval_command(
        TODO_BAD_MAP_VALUE_YASL, TODO_BAD_MAP_VALUE_YASL, "task_list", False
    )


def test_bad_namespace_ref():
    run_eval_command(
        TASK_BAD_NAMESPACE_REF_YASL, TASK_BAD_NAMESPACE_REF_YASL, "task", False
    )


def test_ref_list():
    run_eval_command(REF_LIST_YASL, REF_LIST_YASL, "person_list", True)


def test_namespace_customer_list():
    run_eval_command(
        NAMESPACE_CUSTOMER_LIST_YASL,
        NAMESPACE_CUSTOMER_LIST_YASL,
        "customer_list",
        True,
    )


def test_markdown_rendering():
    run_eval_command(MARKDOWN_YASL, MARKDOWN_YASL, "doc", True)


def test_person_address_multi():
    run_eval_command(
        PERSON_ADDRESS_MULTI_YASL, PERSON_ADDRESS_MULTI_YASL, "person", True
    )


def test_person_website_reachable():
    run_eval_command(
        PERSON_WEBSITE_REACHABLE_YAML, PERSON_WEBSITE_REACHABLE_YAML, "person", True
    )


def test_yasl_eval_api():
    with tempfile.TemporaryDirectory() as tmpdir:
        yaml_path = os.path.join(tmpdir, "test.yaml")
        yasl_path = os.path.join(tmpdir, "test.yasl")
        with open(yaml_path, "w") as f:
            f.write("task_list: {task1: {description: 'task1', complete: true}}")
        with open(yasl_path, "w") as f:
            f.write(TODO_YASL)

        result = yasl_eval(yasl_path, yaml_path, "list_of_tasks")
        assert result is not None


def test_yasl_eval_api_fail():
    with tempfile.TemporaryDirectory() as tmpdir:
        yaml_path = os.path.join(tmpdir, "test.yaml")
        yasl_path = os.path.join(tmpdir, "test.yasl")
        with open(yaml_path, "w") as f:
            f.write(
                "task_list: {task1: {description: 123}}"
            )  # description should be str
        with open(yasl_path, "w") as f:
            f.write(TODO_YASL)

        result = yasl_eval(yasl_path, yaml_path, "list_of_tasks", quiet_log=True)
        assert result is None

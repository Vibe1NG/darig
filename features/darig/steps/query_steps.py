import os
import subprocess
from typing import Any

from behave import given as _given
from behave import then as _then
from behave import when as _when

from darig.query.engine import DarigQueryEngine

# Type cast behave decorators to Any to avoid "Object of type '_StepDecorator' is not callable" errors
given: Any = _given
when: Any = _when
then: Any = _then


@given('a Darig schema "{schema_file}" is loaded')
def step_impl_load_schema(context, schema_file):
    if not hasattr(context, "engine"):
        context.engine = DarigQueryEngine()
    # Path relative to project root
    abs_path = os.path.abspath(schema_file)
    assert context.engine.load_schema(abs_path) is True


@given('YAML data "{data_file}" is loaded')
def step_impl_load_data(context, data_file):
    abs_path = os.path.abspath(data_file)
    assert context.engine.load_data(abs_path) > 0


@when('I run the Darig query "{query}"')
def step_impl_run_query(context, query):
    context.results = context.engine.execute_sql(query)


@then("the query should return {count} row")
@then("the query should return {count} rows")
def step_impl_check_row_count(context, count):
    assert len(context.results) == int(count)


@then('the row should contain "{text}"')
def step_impl_check_row_content(context, text):
    found = False
    for row in context.results:
        if any(text in str(v) for v in row.values()):
            found = True
            break
    assert found is True


@when('I run the Darig query CLI with "{args}"')
def step_impl_run_query_cli(context, args):
    cmd = ["darig", "query"] + args.split()
    # We use communicate to send 'exit' immediately if it's interactive
    process = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    stdout, stderr = process.communicate(input="exit\n")
    context.cli_stdout = stdout
    context.cli_stderr = stderr
    context.cli_returncode = process.returncode


@then('the CLI should show the welcome message "{message}"')
def step_impl_check_cli_output(context, message):
    assert message in context.cli_stdout

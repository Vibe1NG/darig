import sys
from io import StringIO
from darig.schema.core import darig_eval
from pathlib import Path

yasl_path = "./features/darig/schema/data/dir_test"
yaml_path = "./features/darig/schema/data/dir_test"

test_log = StringIO()
results = darig_eval(
    yasl_path,
    yaml_path,
    None,
    verbose_log=True,
    output="text",
    log_stream=test_log,
)

print(f"Results: {results}")
print("--- LOG ---")
print(test_log.getvalue())

"""
Darig Schema - Data validation and schema enforcement

Darig Schema is an advanced schema language & validation tool for YAML data.
It supports definition and validation of data structures with primitives, enumerations, and composition of defined types.
It also supports references between types and properties, enabling complex data models.
"""

from darig.schema.cache import get_darig_schema_registry
from darig.schema.core import (
    check_paths,
    check_schema,
    darig_eval,
    darig_schema_version,
    load_data,
    load_data_files,
    load_schema,
    load_schema_files,
)

# Aliases for backward compatibility
yasl_eval = darig_eval
yasl_version = darig_schema_version

__all__ = [
    "darig_eval",
    "darig_schema_version",
    "yasl_eval",
    "yasl_version",
    "check_paths",
    "check_schema",
    "load_schema",
    "load_schema_files",
    "load_data",
    "load_data_files",
    "get_darig_schema_registry",
]

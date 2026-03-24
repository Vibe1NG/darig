"""
Darig Query - SQL-based query interface for YAML data

Darig Query provides a standard SQL query interface for YAML data.
It dynamically loads YAML data into an in-memory SQLite database, allowing users to execute SQL queries against the data.
Darig Query generated database schemas are derived from Darig Schema definitions, ensuring data integrity and consistency.
"""

from darig.query.engine import (
    DarigQueryEngine,
    export_data,
    get_session,
    load_data,
    load_schema,
)

# Alias for backward compatibility
YaqlEngine = DarigQueryEngine

__all__ = [
    "get_session",
    "load_schema",
    "load_data",
    "export_data",
    "DarigQueryEngine",
    "YaqlEngine",
]

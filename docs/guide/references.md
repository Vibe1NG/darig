# Using References in Darig

Darig allows you to create relationships between different data types using the `ref[Target]` syntax. This ensures referential integrity across your data, validating that a referenced value actually exists in the target collection.
...
*   `TargetType` is the name of the Darig type you are referencing.
...
## How It Works

When Darig validates your data:

1.  **First Pass (Individual Validation):** It checks that all fields match their basic types (e.g., `int`, `str`).
2.  **Reference Resolution:** It identifies all fields using the `ref[...]` type.
3.  **Integrity Check:** It scans the entire dataset to ensure that every `ref[Target.Property]` value has a corresponding match in the `Target` type's `Property` list.

This guarantees that your data is not only syntactically correct but also relationally consistent.

# Design Specification: Darig (Data Rigor)

## Overview
Renaming "Advanced YAML" to "Darig" (Data Rigor) and consolidating its core tools into a single, unified command-line interface and Python package.

## Goals
- Rename the project from `advanced-yaml` to `darig`.
- Unify `yasl` (schema) and `yaql` (query) functionality under the `darig` command.
- Remove obsolete tools `yarl` (reporting) and `yatl` (transformation).
- Simplify the Python package structure for better maintainability.

## Architecture

### Package Structure
The new package structure will be consolidated under `src/darig/`:

- `src/darig/`
    - `__init__.py`
    - `cli.py`: Main entry point for the `darig` command.
    - `schema/`: Core logic for YASL schema validation.
    - `query/`: Core logic for YAQL data querying.
    - `common/`: Shared utilities, versioning, and unified error handling.

### Removed Components
- `src/yarl/`
- `src/yatl/`
- `tests/yarl/`
- `tests/yatl/`
- `features/yarl/`
- `features/yatl/`

## CLI Specification

The `darig` command will be the single entry point:

### `darig check <paths> [--model <model_name>]`
- **Purpose**: Validates YAML data against schemas.
- **Paths**: List of files or directories to check.
- **Model**: Optional specific schema type to validate against.

### `darig schema <path>`
- **Purpose**: Validates that a schema file is correctly defined.

### `darig query [--sql "<query>"] [--schema <path>] [--data <path>] [--interactive]`
- **Purpose**: Query YAML data using SQL-like syntax.
- **Direct execution**: Use `--sql` to run a query and exit.
- **Interactive mode**: If `--interactive` is provided (or no `--sql` is given), enter the `yaql` shell.

### Global Flags
- `--version`: Show "Darig v0.5.0" (or current version).
- `--quiet`/`--verbose`: Control output detail levels.
- `--output [text|json|yaml]`: Set output format (where applicable).

## Implementation Details

### Renaming & Refactoring
- Move logic from `src/yasl` to `src/darig/schema`.
- Move logic from `src/yaql` to `src/darig/query`.
- Consolidate `src/common` into `src/darig/common`.
- Update all internal imports from `yasl.*` or `yaql.*` to `darig.*`.

### Documentation Updates
- Update `README.md` with new "Darig" branding and vision.
- Update `AGENTS.md` with new command names and package structure.
- Update `pyproject.toml` project name and scripts.
- Update `mkdocs.yml` and all files in `docs/` to reflect the rename and tool consolidation.

### Infrastructure & CI/CD
- Update GitHub Workflows (`.github/workflows/*.yml`) to reference `darig` instead of `yasl` or `yaql`.
- Update support scripts like `scripts/bash/verify_prod_deps.sh` to use the new `darig` command.

### Test Updates
- Rename `tests/yasl` -> `tests/darig/schema`.
- Rename `tests/yaql` -> `tests/darig/query`.
- Update BDD feature files in `features/` to use `darig` command syntax.

## Success Criteria
1. `darig --version` returns correctly.
2. `darig check` and `darig query` pass all existing unit tests.
3. `yarl` and `yatl` are removed from the codebase.
4. All documentation correctly refers to "Darig" and its subcommands.

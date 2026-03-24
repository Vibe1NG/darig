# Darig (Data Rigor) Restructure Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rename "Advanced YAML" to "Darig", consolidate `yasl` and `yaql` into a single `darig` command, and remove obsolete tools.

**Architecture:**
- Rename `advanced-yaml` project to `darig`.
- Restructure `src/yasl` and `src/yaql` into submodules of `src/darig/`.
- Unify all CLI entry points into `src/darig/cli.py`.
- Remove `yarl` and `yatl` tools and tests.
- Update CI/CD and docs to reflect the new "Darig" identity.

**Tech Stack:**
- Python 3.12+
- `uv` for project management.
- `argparse` (or `click` if preferred, but existing code uses `argparse`) for the unified CLI.
- `ruamel-yaml`, `pydantic`.

---

### Task 1: Project Metadata & Initial Cleanup

**Files:**
- Modify: `pyproject.toml`
- Modify: `AGENTS.md`
- Modify: `README.md`
- Delete: `src/yarl/`
- Delete: `src/yatl/`
- Delete: `tests/yarl/`
- Delete: `tests/yatl/`
- Delete: `features/yarl/`
- Delete: `features/yatl/`

- [ ] **Step 1: Update Project Metadata in `pyproject.toml`**
  - Change project name to `darig`.
  - Update `[project.scripts]` to define `darig = "darig.cli:main"`.
  - Remove `yasl`, `yaql`, `yarl`, and `yatl` scripts.
- [ ] **Step 2: Update `AGENTS.md` and `README.md`**
  - Replace "Advanced YAML" with "Darig".
  - Update CLI command documentation to use `darig`.
- [ ] **Step 3: Remove obsolete tools**
  - Delete `src/yarl/`, `src/yatl/`, `tests/yarl/`, `tests/yatl/`, `features/yarl/`, `features/yatl/`.
- [ ] **Step 4: Commit**
  ```bash
  git add pyproject.toml AGENTS.md README.md
  git rm -r src/yarl src/yatl tests/yarl tests/yatl features/yarl features/yatl
  git commit -m "chore: rename project to darig and remove obsolete tools"
  ```

---

### Task 2: Package Restructuring

**Files:**
- Create: `src/darig/`
- Create: `src/darig/__init__.py`
- Create: `src/darig/common/`
- Create: `src/darig/schema/`
- Create: `src/darig/query/`
- Move: `src/common/*` -> `src/darig/common/`
- Move: `src/yasl/*` -> `src/darig/schema/`
- Move: `src/yaql/*` -> `src/darig/query/`

- [ ] **Step 1: Create new directory structure**
  - Run: `mkdir -p src/darig/common src/darig/schema src/darig/query`
- [ ] **Step 2: Move files and update imports**
  - Move `src/common/*.py` to `src/darig/common/`.
  - Move `src/yasl/*.py` to `src/darig/schema/`.
  - Move `src/yaql/*.py` to `src/darig/query/`.
  - Update `src/darig/schema/__init__.py` and `src/darig/query/__init__.py` to re-export core functions (`check_paths`, `check_schema`, `YaqlEngine`, etc.).
  - Update all internal imports from `yasl.*` to `darig.schema.*`, `yaql.*` to `darig.query.*`, and `common.*` to `darig.common.*`.
- [ ] **Step 3: Update versioning in `src/darig/common/utils.py`**
  - Ensure versioning logic references the `darig` package.
- [ ] **Step 4: Commit**
  ```bash
  git add src/darig
  git commit -m "refactor: restructure packages under darig/ namespace"
  ```

---

### Task 3: CLI Unification

**Files:**
- Create: `src/darig/cli.py`

- [ ] **Step 1: Implement unified CLI in `src/darig/cli.py`**
  - Combine logic from `src/darig/schema/cli.py` and `src/darig/query/cli.py` into a single `argparse` structure.
  - Define global flags: `--version`, `--quiet`, `--verbose`, `--output` at the main parser level.
  - Implement subcommands: `check`, `schema`, `query`.
  - `darig check` -> calls `darig.schema.check_paths`.
  - `darig schema` -> calls `darig.schema.check_schema`.
  - `darig query` -> supports flags: `--sql`, `--interactive`, `--schema`, `--data`.
    - If `--sql` is provided, execute query and print results (reusing result-printing logic from `YaqlShell`).
    - If `--interactive` (or no `--sql`), start `YaqlShell`.
  - Ensure all subcommands pass their relevant global flags (quiet, verbose, etc.) down to the engine/core logic.
- [ ] **Step 2: Migrate shell logic and remove old CLI files**
  - Move `YaqlShell` class and any other core CLI logic from `src/darig/query/cli.py` and `src/darig/schema/cli.py` into `src/darig/cli.py`.
  - Delete `src/darig/schema/cli.py` and `src/darig/query/cli.py`.
- [ ] **Step 3: Verify basic CLI functionality**
  - Run: `uv run darig --version`
  - Run: `uv run darig --help`
- [ ] **Step 4: Commit**
  ```bash
  git add src/darig/cli.py
  git commit -m "feat: add unified darig CLI"
  ```

---

### Task 4: Test & Feature Refactoring

**Files:**
- Rename: `tests/yasl` -> `tests/darig/schema`
- Rename: `tests/yaql` -> `tests/darig/query`
- Modify: `features/*.feature`
- Modify: `tests/conftest.py`

- [ ] **Step 1: Move and update tests**
  - Rename test directories.
  - Update all imports in tests to reflect the new `darig.*` namespace.
- [ ] **Step 2: Update BDD feature files**
  - Replace all `yasl` and `yaql` command calls with `darig <subcommand>`.
- [ ] **Step 3: Run all tests**
  - Run: `uv run pytest`
  - Run: `uv run behave`
- [ ] **Step 4: Commit**
  ```bash
  git add tests features
  git commit -m "test: update tests and features for darig rename"
  ```

---

### Task 5: Infrastructure & Documentation Update

**Files:**
- Modify: `.github/workflows/*.yml`
- Modify: `mkdocs.yml`
- Modify: `docs/**/*.md`
- Modify: `scripts/bash/verify_prod_deps.sh`

- [ ] **Step 1: Update GitHub Workflows**
  - Replace `yasl-ci.yml` with `darig-ci.yml`.
  - Update all references to `advanced-yaml` and sub-tools.
- [ ] **Step 2: Update mkdocs and documentation**
  - Update `mkdocs.yml` site name and navigation.
  - Search and replace "Advanced YAML" with "Darig" across all files in `docs/`.
  - Update any tool usage examples in documentation.
- [ ] **Step 3: Update support scripts**
  - Update `scripts/bash/verify_prod_deps.sh` to use `darig` command.
- [ ] **Step 4: Final verification**
  - Run: `./ci.sh all` (or equivalent) to ensure everything passes.
- [ ] **Step 5: Commit**
  ```bash
  git add .github mkdocs.yml docs scripts
  git commit -m "docs: update branding and infrastructure for Darig"
  ```

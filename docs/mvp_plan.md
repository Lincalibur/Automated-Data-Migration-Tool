# MVP Plan: Automated Data Migration Tool

## Context

This is a portfolio project (Flask ETL/conversion tool) that recruiters/interviewers will look at and try. It currently works for its two hardcoded conversions, but has real holes that undercut "functional product" credibility: arbitrary file read/write via unvalidated paths, an arbitrary-database-connection-string `/migrate` endpoint that's not reachable from the UI at all, no CI test execution, and hardcoded `debug=True`. Scope for this MVP pass: **polished single-user portfolio demo** — no auth/multi-tenancy, no job queue/Docker, migrations stay synchronous. The goal is: every advertised feature is reachable from the UI, the obvious security holes are closed, and CI actually proves the test suite passes.

## Changes

### 1. Path/security hardening (`src/main.py`)

- Add a `_safe_path(base_dir, path)` helper: resolves `path` against `base_dir` using `os.path.realpath`, raises/returns `None` if the result isn't contained in `base_dir` (via `os.path.commonpath`). Used to validate:
  - `/upload`: run `file.filename` through Werkzeug's `secure_filename()` before joining to `UPLOAD_FOLDER`.
  - `/convert`: validate `file_path` is inside `UPLOAD_FOLDER` before opening it.
  - `/migrate`: when `source`/`destination` type is `"file"`, validate the path is inside `UPLOAD_FOLDER` (source) or `OUTPUT_FOLDER` (destination).
- `/migrate` database connections: restrict `connection_string` to the `sqlite:///` scheme only, and resolve the target `.db` file path through the same `_safe_path` check against `OUTPUT_FOLDER`. Reject anything else with a 400. This keeps the ETL demo fully working (file↔sqlite) while closing the "connect to arbitrary database" hole.
- Add `app.config['MAX_CONTENT_LENGTH']` (e.g. 20 MB) so oversized uploads get a clean 413 instead of an unbounded memory read.
- `main()`: read debug mode from an env var (`ADMT_DEBUG`, default `False`) instead of hardcoding `debug=True`. Document in README that `python src/main.py` runs in production-safe mode by default; set `ADMT_DEBUG=1` for local dev with the reloader/debugger.

### 2. Expose `/migrate` in the UI

- `src/ui/templates/index.html`: add a second panel ("Migrate data") alongside the existing convert panel:
  - Reuses the existing dropzone/upload flow to get a source file path.
  - Destination type select: "Download as file" (format dropdown: csv/xlsx/json) or "Save to local database" (table name input; connection string is fixed server-side to `output_files/warehouse.db`, not user-entered — keeps the safe-path restriction simple and avoids exposing raw connection strings in the UI).
  - Optional column mapping: a small repeatable "source column → destination column" row pair, serialized into the `field_map` dict sent to `/migrate`.
- `src/ui/static/app.js`: add the corresponding fetch call to `/migrate` with the assembled JSON body, mirroring the existing `convertBtn` handler; render success/error via the existing `showResult()`.
- `src/ui/static/style.css`: extend existing dropzone/panel styles for the new form elements (reuse existing classes where possible, e.g. `.uploaded-info`, `.result`).

This also satisfies "generic converter" — since `/migrate` already supports file→file across csv/xlsx/json/db in any direction, exposing it in the UI gives users arbitrary tabular format conversion for free, without adding new entries to `CONVERTIBLES`.

### 3. CI

- Add `.github/workflows/tests.yml`: on push/PR to any branch, checkout, set up Python 3.12, `pip install -r requirements.txt`, run `pytest tests/ -v`. This is the highest-value change for credibility — right now nothing actually runs the test suite. Leave `display-file-structure.yml` and `manual-setup.yml` as-is (out of scope).

### 4. Tests (`tests/`)

- `tests/test_ui.py`: add cases for the hardened paths —
  - `/convert` with a `file_path` outside `uploaded_files/` (e.g. `../../etc/passwd`-style) returns 400.
  - `/upload` with a traversal filename (`../evil.txt`) is sanitized and saved inside `UPLOAD_FOLDER` only.
  - `/migrate` with a non-sqlite or path-escaping `connection_string` returns 400.
  - `/migrate` end-to-end through the safe path (file → sqlite in `output_files/`) succeeds, extending the existing `test_etl.py` coverage at the route level.
- Keep `tests/conftest.py`'s `sys.path` shim as-is; new tests follow the existing `client()` helper pattern in `test_ui.py`.

### 5. README

- Update the "Notes on scope" section: remove/adjust the "no auth on the API" caveat to reflect the new path/connection restrictions, document `ADMT_DEBUG`, and add the Migrate UI to the feature list and usage walkthrough.

## Out of scope (explicitly, per MVP scope decision)

- Auth/API keys, multi-user accounts.
- Background job queue / async migrations — stays synchronous with the new `MAX_CONTENT_LENGTH` cap as the mitigation.
- Docker/deployment config, cloud storage connectors.
- Type coercion / advanced transform rules in `DataTransformer`.

## Verification

1. `pytest tests/ -v` — all existing + new tests pass.
2. Manually run `python src/main.py`, open `http://127.0.0.1:5000/`:
   - Convert panel: upload the existing `uploaded_files/sample.pdf`, convert to Word, confirm download link works (regression check).
   - Migrate panel: upload a small CSV, map a column, submit to "Save to local database", confirm success message and that `output_files/warehouse.db` contains the table; repeat with "Download as file" (e.g. to xlsx) and confirm the file downloads correctly.
   - Attempt a crafted `/convert` request via curl with a `file_path` outside `uploaded_files/` and confirm 400.
3. Push to a branch and confirm the new GitHub Actions workflow runs and passes.

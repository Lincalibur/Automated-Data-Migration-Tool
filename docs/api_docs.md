# API Reference

Base URL: `http://127.0.0.1:5000`

## `GET /`

Renders the web UI (drag-and-drop upload + conversion picker).

## `POST /upload`

Uploads a file to be used by `/convert` or `/migrate`.

- Body: `multipart/form-data` with a `file` field.
- Response `200`: `{"message": "...", "file_path": "<absolute path on disk>"}`
- Response `400`: `{"error": "No file provided"}` if the `file` field is missing.

## `POST /convert`

Runs one of the predefined single-file conversions from `src/convertibles.py`.

- Body (JSON): `{"file_path": "...", "convert_to": "pdf_to_word" | "sql_to_excel"}`
- `pdf_to_word`: `file_path` should be a `.pdf`; produces a `.docx` in `output_files/`.
- `sql_to_excel`: `file_path` should be a SQLite `.db` file; exports its first
  table to a `.xlsx` in `output_files/`.
- Response `200`: `{"message": "...", "destination_file": "..."}`
- Response `400`: unknown `convert_to`, missing fields, or source file not found.
- Response `500`: the converter itself raised an error (message included).

## `POST /migrate`

Runs a generic extract → transform → load pipeline.

- Body (JSON):
  ```json
  {
    "source": {"type": "file", "path": "..."},
    "destination": {"type": "database", "connection_string": "sqlite:///...", "table": "..."},
    "field_map": {"source_column": "destination_column"}
  }
  ```
  `source`/`destination` `type` is `"file"` (needs `path`) or `"database"`
  (needs `connection_string` + `table`). `field_map` is optional; omit it to
  pass columns through unchanged.
- Response `200`: `{"message": "...", "rows_migrated": <int>}`
- Response `400`: missing `source`/`destination`.
- Response `500`: extraction/transform/load raised an error (message included) —
  e.g. an unsupported file extension, a missing table, or a `field_map` that
  references a column not present in the source data.

## `GET /output_files/<filename>`

Downloads a file produced by `/convert` or a file-destination `/migrate` call.

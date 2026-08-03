# User Guide

## Converting a single file (web UI)

1. Start the app: `python src/main.py`, then open `http://127.0.0.1:5000/`.
2. Drag a file onto the dropzone, or click it to browse.
3. Pick a conversion from the dropdown:
   - **pdf to word** — expects a `.pdf`, produces a `.docx`.
   - **sql to excel** — expects a SQLite `.db` file, exports its first table
     to `.xlsx`.
4. Click **Convert**. The resulting file path (inside `output_files/`) is
   shown on success; download it via `GET /output_files/<filename>`.

## Migrating data between a file and a database

Use the `/migrate` endpoint (see `docs/api_docs.md`) when you want to move
rows — not just convert a single file — between:

- a CSV/Excel/JSON file and a database table, in either direction, or
- two database tables, or
- two files (e.g. re-mapping columns while going CSV → Excel).

Example: import a CSV of customers into a local SQLite database, renaming
columns as you go:

```bash
curl -X POST http://127.0.0.1:5000/upload -F "file=@customers.csv"
# => {"file_path": "C:\\...\\uploaded_files\\customers.csv", ...}

curl -X POST http://127.0.0.1:5000/migrate \
  -H "Content-Type: application/json" \
  -d '{
        "source": {"type": "file", "path": "C:\\...\\uploaded_files\\customers.csv"},
        "destination": {"type": "database", "connection_string": "sqlite:///C:/.../output_files/warehouse.db", "table": "customers"},
        "field_map": {"cust_name": "customer_name", "cust_email": "email"}
      }'
```

Use the exact `file_path` returned by `/upload` — it's an absolute path, which
avoids ambiguity about what directory it's resolved against.

## Running it as a library

The ETL classes can also be used directly from Python, without the web layer:

```python
from etl.extract import DataExtractor
from etl.transform import DataTransformer
from etl.load import DataLoader

data = DataExtractor({"type": "file", "path": "customers.csv"}).extract()
transformed = DataTransformer(field_map={"cust_name": "customer_name"}).transform(data)
DataLoader({"type": "database", "connection_string": "sqlite:///warehouse.db", "table": "customers"}).load(transformed)
```

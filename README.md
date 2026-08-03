# Automated Data Migration Tool (ADMT)

A small Flask application for moving and converting tabular data between files
and databases. It supports two workflows:

- **One-off file conversion** — upload a file through the web UI and convert it
  (PDF → Word, or a SQLite table → Excel).
- **Generic ETL migration** — extract data from a file or database, optionally
  remap/rename columns, and load it into a different file or database, via the
  `/migrate` API.

## Features

- **Web UI**: drag-and-drop (or click-to-browse) file upload with in-browser
  conversion, served directly by Flask — no separate frontend build required.
- **File ⇄ database ETL pipeline**: `DataExtractor` → `DataTransformer` →
  `DataLoader` classes that read/write CSV, Excel, JSON files and any
  SQLAlchemy-supported database (SQLite by default, no server setup needed).
- **Column mapping**: `FieldMapper` renames and selects columns between a
  source and destination schema during migration.
- **File converters**: PDF → Word (`pypdf` + `python-docx`), SQLite table →
  Excel (`SQLAlchemy` + `pandas`/`openpyxl`).
- **Tested**: `pytest` suite covering the converters, the ETL pipeline
  (file→database and database→file), the field mapper, and the Flask routes.

## Getting Started

### Prerequisites

- Python 3.9+

### Installation

```bash
git clone https://github.com/Lincalibur/Automated-Data-Migration-Tool.git
cd Automated-Data-Migration-Tool
python -m venv .venv
.venv\Scripts\activate   # macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

### Running the app

```bash
python src/main.py
```

Then open `http://127.0.0.1:5000/` and drag in a `.pdf` (converts to `.docx`)
or a SQLite `.db` file (exports its first table to `.xlsx`).

### Running the tests

```bash
pytest tests/ -v
```

## API

| Route        | Method | Purpose                                                       |
|--------------|--------|----------------------------------------------------------------|
| `/`          | GET    | Web UI                                                         |
| `/upload`    | POST   | Upload a file (multipart form, field name `file`)               |
| `/convert`   | POST   | Convert an uploaded file: `{"file_path": ..., "convert_to": "pdf_to_word" \| "sql_to_excel"}` |
| `/migrate`   | POST   | Run an extract → transform → load pipeline (see below)         |

### `/migrate` example

Move a CSV file into a SQLite table, renaming columns along the way:

```bash
curl -X POST http://127.0.0.1:5000/migrate \
  -H "Content-Type: application/json" \
  -d '{
        "source": {"type": "file", "path": "uploaded_files/customers.csv"},
        "destination": {
          "type": "database",
          "connection_string": "sqlite:///output_files/warehouse.db",
          "table": "customers"
        },
        "field_map": {"cust_name": "customer_name", "cust_email": "email"}
      }'
```

`source`/`destination` each take `{"type": "file", "path": "..."}` or
`{"type": "database", "connection_string": "...", "table": "..."}`. SQLite
connection strings with a relative path are resolved relative to the
directory the server was started from — use an absolute path if you're
calling the API from somewhere else.

## Project structure

```
Automated-Data-Migration-Tool/
├── docs/                     # API and usage notes
├── src/
│   ├── main.py                # Flask app: routes for upload/convert/migrate
│   ├── convertibles.py         # Registry of supported one-off conversions
│   ├── converters/             # pdf_to_word, sql_to_excel
│   ├── data_sources/           # FileConnector, DatabaseConnector
│   ├── etl/                    # DataExtractor, DataTransformer, DataLoader
│   ├── mapping/                # FieldMapper
│   └── ui/                     # templates/ + static/ for the web UI
├── tests/                    # pytest suite
├── requirements.txt
└── setup.py
```

## Notes on scope

This is a portfolio/learning project, not a production migration tool: there's
no auth on the API, no background job queue for large migrations, and no
cloud storage connectors (S3/GCS/etc.) — only local files and SQLAlchemy
databases. Everything listed above is implemented and tested; nothing here is
a stub.

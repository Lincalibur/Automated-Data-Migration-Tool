# src/data_sources/file_connector.py
import os
import pandas as pd


class FileConnector:
    """Reads and writes tabular data (CSV, Excel, JSON) using pandas."""

    READERS = {
        '.csv': pd.read_csv,
        '.xlsx': pd.read_excel,
        '.xls': pd.read_excel,
        '.json': pd.read_json,
    }

    def read(self, file_path):
        """Read a tabular file into a pandas DataFrame based on its extension."""
        ext = os.path.splitext(file_path)[1].lower()
        reader = self.READERS.get(ext)
        if reader is None:
            raise ValueError(f"Unsupported file type for reading: {ext}")
        return reader(file_path)

    def write(self, file_path, data):
        """Write a pandas DataFrame to a tabular file based on its extension."""
        ext = os.path.splitext(file_path)[1].lower()
        os.makedirs(os.path.dirname(file_path) or '.', exist_ok=True)
        if ext == '.csv':
            data.to_csv(file_path, index=False)
        elif ext in ('.xlsx', '.xls'):
            data.to_excel(file_path, index=False)
        elif ext == '.json':
            data.to_json(file_path, orient='records', indent=2)
        else:
            raise ValueError(f"Unsupported file type for writing: {ext}")
        return file_path

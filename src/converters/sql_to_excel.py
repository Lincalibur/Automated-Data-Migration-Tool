# src/converters/sql_to_excel.py
from data_sources.database_connector import DatabaseConnector
from data_sources.file_connector import FileConnector


def sql_to_excel_converter(db_file_path, excel_file_path, table_name=None):
    """Convert a table in a SQLite database file to an Excel spreadsheet.

    :param db_file_path: path to a .db/.sqlite file.
    :param excel_file_path: path to write the resulting .xlsx file.
    :param table_name: table to export; defaults to the first table found.
    """
    connector = DatabaseConnector(f"sqlite:///{db_file_path}")
    if table_name is None:
        tables = connector.list_tables()
        if not tables:
            raise ValueError(f"No tables found in database: {db_file_path}")
        table_name = tables[0]

    data = connector.read_table(table_name)
    FileConnector().write(excel_file_path, data)
    print(f"Converted table '{table_name}' in {db_file_path} to {excel_file_path}")
    return excel_file_path

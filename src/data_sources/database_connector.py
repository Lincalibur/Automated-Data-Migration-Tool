# src/data_sources/database_connector.py
import pandas as pd
from sqlalchemy import create_engine


class DatabaseConnector:
    """Thin wrapper around SQLAlchemy for reading/writing whole tables as DataFrames.

    Works with any SQLAlchemy connection string; defaults to a local SQLite
    file so the tool is usable out of the box without standing up a real
    database server.
    """

    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.engine = create_engine(connection_string)

    def read_table(self, table_name):
        with self.engine.connect() as conn:
            return pd.read_sql_table(table_name, conn)

    def write_table(self, table_name, data, if_exists='replace'):
        with self.engine.connect() as conn:
            data.to_sql(table_name, conn, if_exists=if_exists, index=False)
            conn.commit()
        return table_name

    def list_tables(self):
        from sqlalchemy import inspect
        return inspect(self.engine).get_table_names()

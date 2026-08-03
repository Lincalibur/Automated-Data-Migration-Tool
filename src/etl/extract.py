# src/etl/extract.py
from data_sources.database_connector import DatabaseConnector
from data_sources.file_connector import FileConnector


class DataExtractor:
    def __init__(self, source_config):
        """
        :param source_config: dict describing the source, e.g.
            {'type': 'file', 'path': 'input.csv'}
            {'type': 'database', 'connection_string': 'sqlite:///data.db', 'table': 'customers'}
        """
        self.source_config = source_config

    def extract(self):
        """Extract data based on self.source_config, dispatching to the right method."""
        source_type = self.source_config.get('type')
        if source_type == 'database':
            return self.extract_from_database()
        if source_type == 'file':
            return self.extract_from_file(self.source_config['path'])
        raise ValueError(f"Unknown source type: {source_type}")

    def extract_from_database(self):
        """Extract a table from a database source into a DataFrame."""
        connector = DatabaseConnector(self.source_config['connection_string'])
        return connector.read_table(self.source_config['table'])

    def extract_from_file(self, file_path):
        """Extract tabular data from a file source into a DataFrame."""
        connector = FileConnector()
        return connector.read(file_path)

# src/etl/load.py
from data_sources.database_connector import DatabaseConnector
from data_sources.file_connector import FileConnector


class DataLoader:
    def __init__(self, destination_config):
        """
        :param destination_config: dict describing the destination, e.g.
            {'type': 'file', 'path': 'output.xlsx'}
            {'type': 'database', 'connection_string': 'sqlite:///data.db', 'table': 'customers'}
        """
        self.destination_config = destination_config

    def load(self, data):
        """Load data based on self.destination_config, dispatching to the right method."""
        dest_type = self.destination_config.get('type')
        if dest_type == 'database':
            return self.load_to_database(data)
        if dest_type == 'file':
            return self.load_to_file(self.destination_config['path'], data)
        raise ValueError(f"Unknown destination type: {dest_type}")

    def load_to_database(self, data):
        """Load a DataFrame into a database table destination."""
        connector = DatabaseConnector(self.destination_config['connection_string'])
        return connector.write_table(self.destination_config['table'], data)

    def load_to_file(self, file_path, data):
        """Load a DataFrame into a file destination."""
        connector = FileConnector()
        return connector.write(file_path, data)

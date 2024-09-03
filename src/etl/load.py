# src/etl/load.py
class DataLoader:
    def __init__(self, destination_config):
        """
        Initialize the data loader with the given destination configuration.
        
        :param destination_config: Dictionary containing destination configuration details.
        """
        self.destination_config = destination_config

    def load_to_database(self, data):
        """
        Load data into a database destination.
        
        :param data: Data to be loaded.
        """
        # Placeholder for database loading logic
        print("Loading data to database...")
        # Implement actual database loading logic here

    def load_to_file(self, file_path, data):
        """
        Load data into a file destination.
        
        :param file_path: Path to the destination file.
        :param data: Data to be loaded.
        """
        # Placeholder for file writing logic
        print(f"Loading data to file: {file_path}...")
        # Implement actual file writing logic here

import os

import pandas as pd

from etl.extract import DataExtractor
from etl.load import DataLoader
from etl.transform import DataTransformer
from data_sources.database_connector import DatabaseConnector


def test_file_to_database_pipeline(tmp_path):
    csv_path = tmp_path / 'customers.csv'
    pd.DataFrame({
        'cust_name': ['Alice', 'Bob', None],
        'cust_email': ['alice@example.com', 'bob@example.com', None],
    }).to_csv(csv_path, index=False)

    db_path = tmp_path / 'warehouse.db'
    connection_string = f"sqlite:///{db_path}"

    data = DataExtractor({'type': 'file', 'path': str(csv_path)}).extract()
    transformed = DataTransformer(field_map={'cust_name': 'customer_name', 'cust_email': 'email'}).transform(data)
    DataLoader({'type': 'database', 'connection_string': connection_string, 'table': 'customers'}).load(transformed)

    result = DatabaseConnector(connection_string).read_table('customers')
    assert list(result.columns) == ['customer_name', 'email']
    assert result['customer_name'].tolist() == ['Alice', 'Bob']


def test_database_to_file_pipeline(tmp_path):
    db_path = tmp_path / 'source.db'
    connection_string = f"sqlite:///{db_path}"
    DatabaseConnector(connection_string).write_table(
        'products', pd.DataFrame({'id': [1, 2], 'name': ['Widget', 'Gadget']})
    )

    output_path = tmp_path / 'products.xlsx'

    data = DataExtractor({'type': 'database', 'connection_string': connection_string, 'table': 'products'}).extract()
    transformed = DataTransformer().transform(data)
    DataLoader({'type': 'file', 'path': str(output_path)}).load(transformed)

    assert output_path.exists()
    result = pd.read_excel(output_path)
    assert result['name'].tolist() == ['Widget', 'Gadget']

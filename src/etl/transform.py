# src/etl/transform.py
from mapping.mapper import FieldMapper


class DataTransformer:
    def __init__(self, field_map=None, drop_empty_rows=True):
        """
        :param field_map: optional dict of {source_column: destination_column}
            applied via FieldMapper. Pass None to keep columns as-is.
        :param drop_empty_rows: if True, drop rows that are entirely NaN.
        """
        self.mapper = FieldMapper(field_map)
        self.drop_empty_rows = drop_empty_rows

    def transform(self, data):
        """Apply column mapping and basic cleanup rules to a DataFrame."""
        transformed = self.mapper.apply(data)
        if self.drop_empty_rows:
            transformed = transformed.dropna(how='all')
        return transformed.reset_index(drop=True)

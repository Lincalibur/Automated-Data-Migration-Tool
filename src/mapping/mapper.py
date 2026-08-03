# src/mapping/mapper.py
class FieldMapper:
    """Maps columns from a source schema to a destination schema.

    Example:
        mapper = FieldMapper({'cust_name': 'customer_name', 'cust_email': 'email'})
        mapped_df = mapper.apply(df)
    """

    def __init__(self, field_map=None):
        """
        :param field_map: dict of {source_column: destination_column}. If None
            or empty, columns are passed through unchanged.
        """
        self.field_map = field_map or {}

    def apply(self, data):
        """Rename mapped columns and drop any source column not present in the
        mapping when a mapping is supplied. Unmapped data is returned unchanged.
        """
        if not self.field_map:
            return data

        unknown = [col for col in self.field_map if col not in data.columns]
        if unknown:
            raise KeyError(f"Mapping references columns not present in source data: {unknown}")

        mapped = data.rename(columns=self.field_map)
        return mapped[list(self.field_map.values())]

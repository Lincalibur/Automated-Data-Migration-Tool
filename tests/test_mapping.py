import pandas as pd
import pytest

from mapping.mapper import FieldMapper


def test_apply_with_no_mapping_returns_data_unchanged():
    df = pd.DataFrame({'a': [1, 2], 'b': [3, 4]})
    result = FieldMapper().apply(df)
    pd.testing.assert_frame_equal(result, df)


def test_apply_renames_and_reorders_mapped_columns():
    df = pd.DataFrame({'cust_name': ['Alice', 'Bob'], 'cust_email': ['a@x.com', 'b@x.com'], 'extra': [1, 2]})
    mapper = FieldMapper({'cust_name': 'customer_name', 'cust_email': 'email'})

    result = mapper.apply(df)

    assert list(result.columns) == ['customer_name', 'email']
    assert result['customer_name'].tolist() == ['Alice', 'Bob']
    assert 'extra' not in result.columns


def test_apply_raises_on_unknown_source_column():
    df = pd.DataFrame({'a': [1]})
    mapper = FieldMapper({'missing_column': 'dest'})

    with pytest.raises(KeyError):
        mapper.apply(df)

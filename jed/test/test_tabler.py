from unittest.mock import MagicMock
from unittest.mock import Mock
from unittest.mock import patch

from jed import tabler

TABLES = [["table1"], ["table2"], ["table_3"], ["table_4"]]
UNNESTED_TABLES = ["table1", "table2", "table_3", "table_4"]


@patch("jed.tabler.get_table_names")
def test_get_related_table_names(civis_tables: MagicMock):
    """Should return tables with '_'"""
    civis_tables.return_value = UNNESTED_TABLES
    returned_tables = tabler.get_related_table_names("_", civis_client=MagicMock)

    assert returned_tables == ["table_3", "table_4"]


def test_get_table_id():
    """Should return a table ID"""
    client = Mock()
    client.tables = Mock()
    client.tables.list = Mock()
    client.tables.list.return_value = [{"id": 1, "foo": "a"}, {"id": 2, "foo": "b"}]
    result = tabler.get_table_id("schema", "table_name", client)
    assert result == 1

import civis
from civis.io import read_civis_sql
from jed.utils import get_client


def get_table_names(civis_client: civis.APIClient | None = None) -> list:
    """Return list of table names from Civis"""
    client = get_client(civis_client)
    tables = read_civis_sql(
        "SELECT table_name FROM information_schema.tables",
        client=client,
        database="Ethical Electric",
    )
    return [table[0] for table in tables]


def get_related_table_names(
    topic: str, civis_client: civis.APIClient | None = None
) -> list:
    """Return list of table names related to topic from Civis"""
    client = get_client(civis_client)
    topic_lower = topic.lower()
    tables = get_table_names(client)
    return [table for table in tables if topic_lower in table]


def get_table_id(
    schema: str, table_name: str, civis_client: civis.APIClient | None = None
):
    """Gets table ID from Civis"""
    client = get_client(civis_client)
    t = client.tables.list(
        database_id=36,
        schema=schema,
        name=table_name,
    )
    return t[0]["id"]

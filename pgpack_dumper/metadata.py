from psycopg import Cursor

from .query_template import query_template
from .random_name import random_name


def read_metadata(
    cursor: Cursor,
    query: str | None = None,
    table_name: str | None = None,
) -> bytes:
    """Read metadata for query or table."""

    if not query and not table_name:
        raise ValueError()

    if query:
        session_name = random_name()
        prepare_name = f"{session_name}_prepare"
        table_name = f"{session_name}_temp"
        cursor.execute(query_template("prepare").format(
            prepare_name=prepare_name,
            query=query,
            table_name=table_name,
        ))

    cursor.execute(query_template("attributes").format(
        table_name=table_name,
    ))

    metadata: bytes = cursor.fetchone()[0]

    if query:
        cursor.execute(f"drop table if exists {table_name};")

    return metadata

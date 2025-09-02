from typing import NamedTuple


class PGConnector(NamedTuple):
    """Connector for PostgreSQL."""

    host: str
    dbname: str
    user: str
    password: str
    port: int

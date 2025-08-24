from .query_path import query_path


def query_template(query_name: str) -> str:
    """Get query template for his name."""

    path = query_path().format(query_name)

    with open(path, encoding="utf-8") as query:
        return query.read()

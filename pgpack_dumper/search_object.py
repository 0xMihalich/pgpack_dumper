from re import match


pattern = r"\(select \* from (.*)\)|(.*)"


def search_object(table: str, query: str = "") -> str:
    """Return current string for object."""

    if query:
        return "query"

    return match(pattern, table).group(1) or table

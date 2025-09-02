from pathlib import Path


def query_path() -> str:
    """Path for queryes."""

    return f"{Path(__file__).parent.absolute()}/queryes/{{}}.sql"

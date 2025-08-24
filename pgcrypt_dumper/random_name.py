from random import randbytes


def random_name() -> str:
    """Generate random name for prepare and temp table."""

    return f"session_{randbytes(8).hex()}"  # noqa: S311

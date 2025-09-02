from enum import Enum
from typing import NamedTuple


class RelClass(NamedTuple):
    """Postgres objects."""

    rel_name: str
    is_readobject: bool
    is_readable: bool


class PGObject(RelClass, Enum):
    """RelClass object from relkind value."""

    r = RelClass("Relation table", True, True)
    i = RelClass("Index", False, False)
    S = RelClass("Sequence", False, False)
    t = RelClass("Toast table", False, False)
    v = RelClass("View", False, True)
    m = RelClass("Materialized view", False, True)
    c = RelClass("Composite type", False, False)
    f = RelClass("Foreign table", False, True)
    p = RelClass("Partitioned table", True, True)
    I = RelClass("Partitioned index", False, True)  # noqa: E741
    u = RelClass("Temporary table", True, True)
    o = RelClass("Optimized files", False, False)
    b = RelClass("Block directory", False, False)
    M = RelClass("Visibility map", False, False)

    def __str__(self) -> str:
        """String representation class."""

        return self.rel_name

from io import BufferedReader
from typing import (
    Generator,
    Iterator,
)

from psycopg import (
    Copy,
    Cursor,
)

from .errors import CopyBufferTableNotDefined
from .query_template import query_template
from .metadata import read_metadata


class CopyBuffer:

    def __init__(
        self,
        cursor: Cursor,
        query: str | None = None,
        table_name: str | None = None,
    ) -> None:
        """Class initialization."""

        self.cursor = cursor
        self.query = query
        self.table_name = table_name
        self.pos = 0

    @property
    def metadata(self) -> bytes:
        """Get metadata as bytes."""

        return read_metadata(
            self.cursor,
            self.query,
            self.table_name,
        )

    def copy_to(self) -> Iterator[Copy]:
        """Get copy object from PostgreSQL."""

        if not self.query and not self.table_name:
            raise CopyBufferTableNotDefined()

        if self.query:
            self.table_name = f"({self.query})"

        return self.cursor.copy(
            query_template("copy_to").format(table_name=self.table_name)
        )

    def copy_from(
        self,
        copyobj: BufferedReader,
    ) -> None:
        """Write PGCopy dump into PostgreSQL."""

        if not self.table_name:
            raise CopyBufferTableNotDefined()

        with self.cursor.copy(
            query_template("copy_from").format(table_name=self.table_name)
        ) as cp:
            while chunk := copyobj.read(262_144):
                cp.write(chunk)

    def copy_between(
        self,
        copy_buffer: "CopyBuffer",
    ) -> None:
        """Write from PostgreSQL into PostgreSQL."""

        with copy_buffer.copy_to() as copy_to:
            with self.cursor.copy(
                query_template("copy_from").format(table_name=self.table_name)
            ) as copy_from:
                [copy_from.write(data) for data in copy_to]

    def copy_reader(self, size: int = -1) -> Generator[bytes, None, None]:
        """Read bytes from copy object."""

        with self.copy_to() as copy_object:
            for data in copy_object:
                self.pos += len(data)
                if size != -1 and self.pos >= size:
                    try:
                        end_pos = size % (self.pos - len(data))
                    except ZeroDivisionError:
                        end_pos = size
                    yield data[:end_pos]
                    break
                yield data

    def read(self, size: int = -1) -> bytes:
        """Read bytes from copy object."""

        return b"".join(self.copy_reader(size))

    def tell(self) -> int:
        """Get read size."""

        return self.pos

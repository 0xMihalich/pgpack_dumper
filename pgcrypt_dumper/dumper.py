from io import (
    BufferedReader,
    BufferedWriter,
)

from pgcrypt import (
    CompressionMethod,
    PGCryptReader,
    PGCryptWriter,
)
from psycopg import (
    Connection,
    Cursor,
)

from .copy import CopyBuffer
from .connector import PGConnector
from .errors import PGCryptDumperError


class PGCryptDumper:
    """Class for read and write PGCrypt format."""

    def __init__(
        self,
        connector: PGConnector,
        compression_method: CompressionMethod = CompressionMethod.LZ4,
    ) -> None:
        """Class initialization."""

        try:
            self.connector: PGConnector = connector
            self.connect: Connection = Connection.connect(
                **self.connector._asdict()
            )
            self.cursor: Cursor = self.connect.cursor()
            self.compression_method: CompressionMethod = compression_method
            self.copy_buffer: CopyBuffer = CopyBuffer(self.cursor)
        except Exception as error:
            raise PGCryptDumperError(error)

    def make_buffer_obj(
        self,
        cursor: Cursor | None = None,
        query: str | None = None,
        table_name: str | None = None,
    ) -> CopyBuffer:
        """Make new buffer object for read."""

        return CopyBuffer(
            cursor or Connection.connect(
                **self.connector._asdict()
            ).cursor(),
            query,
            table_name,
        )

    def read_dump(
        self,
        fileobj: BufferedWriter,
        query: str | None = None,
        table_name: str | None = None,
    ) -> None:
        """Read PGCrypt dump from PostgreSQL/GreenPlum."""

        pgcrypt = PGCryptWriter(fileobj, self.compression_method)
        self.copy_buffer.query = query
        self.copy_buffer.table_name = table_name
        pgcrypt.write(
            self.copy_buffer.metadata,
            self.copy_buffer,
        )

    def write_dump(
        self,
        fileobj: BufferedReader,
        table_name: str,
    ) -> None:
        """Write PGCrypt dump into PostgreSQL/GreenPlum."""

        fileobj.seek(0)
        pgcrypt = PGCryptReader(fileobj)
        pgcrypt.pgcopy_compressor.seek(0)
        self.copy_buffer.table_name = table_name
        self.copy_buffer.copy_from(pgcrypt.pgcopy_compressor)
        self.connect.commit()

    def write_between(
        self,
        table_dest: str,
        table_src: str | None = None,
        query_src: str | None = None,
        cursor_src: Cursor | None = None,
    ) -> None:
        """Write from PostgreSQL/GreenPlum into PostgreSQL/GreenPlum."""

        source_copy_buffer = self.make_buffer_obj(
            cursor=cursor_src,
            query=query_src,
            table_name=table_src,
        )
        self.copy_buffer.table_name = table_dest
        self.copy_buffer.copy_between(source_copy_buffer)
        self.connect.commit()

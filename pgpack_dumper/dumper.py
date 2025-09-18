from io import (
    BufferedReader,
    BufferedWriter,
)
from logging import Logger
from types import MethodType

from pgpack import (
    CompressionMethod,
    PGPackReader,
    PGPackWriter,
)
from psycopg import (
    Connection,
    Cursor,
)
from sqlparse import format as sql_format

from .copy import CopyBuffer
from .connector import PGConnector
from .errors import PGPackDumperError
from .logger import DumperLogger
from .multiquery import chunk_query


class PGPackDumper:
    """Class for read and write PGPack format."""

    def __init__(
        self,
        connector: PGConnector,
        compression_method: CompressionMethod = CompressionMethod.LZ4,
        logger: Logger = DumperLogger(),
    ) -> None:
        """Class initialization."""

        try:
            self.connector: PGConnector = connector
            self.connect: Connection = Connection.connect(
                **self.connector._asdict()
            )
            self.cursor: Cursor = self.connect.cursor()
            self.compression_method: CompressionMethod = compression_method
            self.logger = logger
            self.copy_buffer: CopyBuffer = CopyBuffer(self.cursor, self.logger)
        except Exception as error:
            logger.error(error)
            raise PGPackDumperError(error)

        self.version = (
            f"{self.connect.info.server_version // 10000}."
            f"{self.connect.info.server_version % 1000}]"
        )
        self.logger.info(
            f"PGPackDumper initialized for host {self.connector.host}"
            f"[version {self.version}]"
        )

    @staticmethod
    def multiquery(dump_method: MethodType):
        """Multiquery decorator."""

        def wrapper(*args, **kwargs):

            first_part: list[str]
            second_part: list[str]

            self: PGPackDumper = args[0]
            cursor: Cursor = kwargs.get("cursor_src") or self.cursor
            query: str = kwargs.get("query_src") or kwargs.get("query")
            part: int = 1
            first_part, second_part = chunk_query(self.query_formatter(query))
            total_prts = len(sum((first_part, second_part), [])) or 1

            if first_part:
                self.logger.info("Multiquery detected.")

                for query in first_part:
                    self.logger.info(f"Execute query {part}/{total_prts}")
                    cursor.execute(query)
                    part += 1

            if second_part:
                for key in ("query", "query_src"):
                    if key in kwargs:
                        kwargs[key] = second_part.pop(0)
                        break

            self.logger.info(
                f"Execute query {part}/{total_prts}[copy method]"
            )
            dump_method(*args, **kwargs)

            if second_part:
                for query in second_part:
                    part += 1
                    self.logger.info(f"Execute query {part}/{total_prts}")
                    cursor.execute(query)

        return wrapper

    def query_formatter(self, query: str) -> str | None:
        """Reformat query."""

        if not query:
            return
        return sql_format(sql=query, strip_comments=True).strip().strip(";")

    def make_buffer_obj(
        self,
        cursor: Cursor | None = None,
        query: str | None = None,
        table_name: str | None = None,
    ) -> CopyBuffer:
        """Make new buffer object for read."""

        cursor = cursor or Connection.connect(
            **self.connector._asdict()
        ).cursor()
        host = cursor.connection.info.host
        self.logger.info(f"Make new cursor object for host {host}.")

        return CopyBuffer(
            cursor,
            query,
            table_name,
        )

    @multiquery
    def read_dump(
        self,
        fileobj: BufferedWriter,
        query: str | None = None,
        table_name: str | None = None,
    ) -> None:
        """Read PGPack dump from PostgreSQL/GreenPlum."""

        pgpack = PGPackWriter(fileobj, self.compression_method)
        self.copy_buffer.query = query
        self.copy_buffer.table_name = table_name
        pgpack.write(
            self.copy_buffer.metadata,
            self.copy_buffer,
        )

    def write_dump(
        self,
        fileobj: BufferedReader,
        table_name: str,
    ) -> None:
        """Write PGPack dump into PostgreSQL/GreenPlum."""

        fileobj.seek(0)
        pgpack = PGPackReader(fileobj)
        pgpack.pgcopy_compressor.seek(0)
        self.copy_buffer.table_name = table_name
        self.copy_buffer.copy_from(pgpack.pgcopy_compressor)
        self.connect.commit()

    @multiquery
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

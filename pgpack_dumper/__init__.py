"""Library for read and write PGPack format between PostgreSQL and file."""

from pgcopylib import PGCopy
from pgpack import (
    CompressionMethod,
    PGPackReader,
    PGPackWriter,
)

from .connector import PGConnector
from .copy import CopyBuffer
from .dumper import PGPackDumper
from .errors import (
    CopyBufferError,
    CopyBufferObjectError,
    CopyBufferTableNotDefined,
    PGPackDumperError,
    PGPackDumperReadError,
    PGPackDumperWriteError,
    PGPackDumperWriteBetweenError,
)
from .version import __version__


__all__ = (
    "__version__",
    "CompressionMethod",
    "CopyBuffer",
    "CopyBufferError",
    "CopyBufferObjectError",
    "CopyBufferTableNotDefined",
    "PGConnector",
    "PGCopy",
    "PGPackDumper",
    "PGPackDumperError",
    "PGPackDumperReadError",
    "PGPackDumperWriteError",
    "PGPackDumperWriteBetweenError",
    "PGPackReader",
    "PGPackWriter",
)
__author__ = "0xMihalich"

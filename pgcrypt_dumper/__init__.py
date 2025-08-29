"""Library for read and write PGCrypt format between PostgreSQL and file."""

from pgcopylib import PGCopy
from pgcrypt import (
    CompressionMethod,
    PGCryptReader,
    PGCryptWriter,
)

from .connector import PGConnector
from .copy import CopyBuffer
from .dumper import PGCryptDumper
from .errors import (
    CopyBufferError,
    CopyBufferObjectError,
    CopyBufferTableNotDefined,
    PGCryptDumperError,
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
    "PGCryptDumper",
    "PGCryptDumperError",
    "PGCryptReader",
    "PGCryptWriter",
)
__author__ = "0xMihalich"

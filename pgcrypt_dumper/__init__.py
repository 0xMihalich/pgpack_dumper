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
    CopyBufferTableNotDefined,
    PGCryptDumperError,
)

__all__ = (
    "CompressionMethod",
    "CopyBuffer",
    "CopyBufferError",
    "CopyBufferTableNotDefined",
    "PGConnector",
    "PGCopy",
    "PGCryptDumper",
    "PGCryptDumperError",
    "PGCryptReader",
    "PGCryptWriter",
)
__author__ = "0xMihalich"
__version__ = "0.0.2"

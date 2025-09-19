class CopyBufferError(Exception):
    """CopyBuffer base error."""


class CopyBufferObjectError(TypeError):
    """Destination object not support."""


class CopyBufferTableNotDefined(ValueError):
    """Destination table not defined."""


class PGPackDumperError(Exception):
    """PGPackDumper base error."""


class PGPackDumperReadError(PGPackDumperError):
    """PGPackDumper read error."""


class PGPackDumperWriteError(PGPackDumperError):
    """PGPackDumper write error."""


class PGPackDumperWriteBetweenError(PGPackDumperWriteError):
    """PGPackDumper write between error."""

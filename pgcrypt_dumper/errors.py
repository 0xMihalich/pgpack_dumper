class CopyBufferError(Exception):
    """CopyBuffer base error."""


class CopyBufferObjectError(TypeError):
    """Destination object not support."""


class CopyBufferTableNotDefined(ValueError):
    """Destination table not defined."""


class PGCryptDumperError(Exception):
    """PGCryptDumper base error."""

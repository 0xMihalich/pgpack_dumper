class CopyBufferError(Exception):
    """CopyBuffer base error."""


class CopyBufferTableNotDefined(ValueError):
    """Destination table not defined."""


class PGCryptDumperError(Exception):
    """PGCryptDumper base error."""

# PGCryptDumper

Library for read and write PGCrypt format between PostgreSQL and file

## Examples

### Initialization

```python
from pgcrypt_dumper import (
    CompressionMethod,
    PGConnector,
    PGCryptDumper,
)

connector = PGConnector(
    host = <your host>,
    dbname = <your database>,
    user = <your username>,
    password = <your password>,
    port = <your port>,
)

dumper = PGCryptDumper(
    connector=connector,
    compression_method=CompressionMethod.LZ4,  # or CompressionMethod.ZSTD or CompressionMethod.NONE
)
```

### Read dump from PostgreSQL into file

```python
file_name = "pgcrypt.lz4"
# you need define one of parameter query or table_name
query = "select ..."  # some sql query
table_name = "public.test_table"  # some table

with open(file_name, "wb") as fileobj:
    dumper.read_dump(
        fileobj,
        query,
        table_name,
    )
```

### Write dump from file into PostgreSQL

```python
file_name = "pgcrypt.lz4"
# you need define one of parameter table_name
table_name = "public.test_table"  # some table

with open(file_name, "rb") as fileobj:
    dumper.write_dump(
        fileobj,
        table_name,
    )
```

### Write from PostgreSQL into PostgreSQL

Same server

```python

table_dest = "public.test_table_write"  # some table for write
table_src = "public.test_table_read"  # some table for read
query_src = "select ..."  # or some sql query for read

dumper.write_between(
    table_dest,
    table_src,
    query_src,
)
```

Different servers

```python

connector_src = PGConnector(
    host = <host src>,
    dbname = <database src>,
    user = <username src>,
    password = <password src>,
    port = <port src>,
)

dumper_src = PGCryptDumper(connector=connector_src)

table_dest = "public.test_table_write"  # some table for write
table_src = "public.test_table_read"  # some table for read
query_src = "select ..."  # or some sql query for read

dumper.write_between(
    table_dest,
    table_src,
    query_src,
    dumper_src.cursor,
)
```

### Open PGCrypt file format

Get info from my another repository https://github.com/0xMihalich/pgcrypt

## Installation

### From pip

```bash
pip install pgcrypt_dumper
```

### From local directory

```bash
pip install .
```

### From git

```bash
pip install git+https://github.com/0xMihalich/pgcrypt_dumper
```

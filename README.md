# PGPackDumper

Library for read and write PGPack format between PostgreSQL and file

## Examples

### Initialization

```python
from pgpack_dumper import (
    CompressionMethod,
    PGConnector,
    PGPackDumper,
)

connector = PGConnector(
    host = <your host>,
    dbname = <your database>,
    user = <your username>,
    password = <your password>,
    port = <your port>,
)

dumper = PGPackDumper(
    connector=connector,
    compression_method=CompressionMethod.LZ4,  # or CompressionMethod.ZSTD or CompressionMethod.NONE
)
```

### Read dump from PostgreSQL into file

```python
file_name = "pgpack.lz4"
# you need define one of parameter query or table_name
query = "select ..."  # some sql query
table_name = "public.test_table"  # or some table

with open(file_name, "wb") as fileobj:
    dumper.read_dump(
        fileobj,
        query,
        table_name,
    )
```

### Write dump from file into PostgreSQL

```python
file_name = "pgpack.lz4"
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

dumper_src = PGPackDumper(connector=connector_src)

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

### Open PGPack file format

Get info from my another repository https://github.com/0xMihalich/pgpack

## Installation

### From pip

```bash
pip install pgpack_dumper
```

### From local directory

```bash
pip install .
```

### From git

```bash
pip install git+https://github.com/0xMihalich/pgpack_dumper
```

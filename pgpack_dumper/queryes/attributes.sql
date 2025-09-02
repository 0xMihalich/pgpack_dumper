select json_agg(json_build_array(attnum, json_build_array(attname, atttypid::int4))) as metadata
from pg_attribute where attrelid = '{table_name}'::regclass and attnum > 0 and not attisdropped;
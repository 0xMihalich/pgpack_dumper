select json_agg(json_build_array(attnum, json_build_array(attname, atttypid::int4, 
case when atttypid = 1042 then atttypmod - 4 when atttypid = 1700 then (atttypmod - 4) >> 16 else attlen end,
case when atttypid = 1700 then (atttypmod - 4) & 65535 else 0 end, attndims)))::text::bytea as metadata
from pg_attribute where attrelid = '{table_name}'::regclass and attnum > 0 and not attisdropped;
prepare {prepare_name} as {query} limit 0;
drop table if exists {table_name};
create temporary table {table_name} as execute {prepare_name} (null);
deallocate prepare {prepare_name};
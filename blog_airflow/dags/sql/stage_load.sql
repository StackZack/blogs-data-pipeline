BEGIN;
TRUNCATE {{ params.table_name }};
COPY {{ params.table_name }} FROM '{{ params.csv_file_path }}' WITH CSV HEADER;
COMMIT;

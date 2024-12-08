DO $$
BEGIN
    IF NOT EXISTS (
        SELECT FROM pg_database
        WHERE datname = '${POSTGRES_DB}'
    ) THEN
        PERFORM dblink_exec(
            'dbname=postgres user=${POSTGRES_USER} password=${POSTGRES_PASSWORD}',
            'CREATE DATABASE ${POSTGRES_DB} OWNER ${POSTGRES_USER};'
        );
    END IF;
END
$$;
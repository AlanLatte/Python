"""Automatically truncate all tables before each test."""

import pytest

from app.internal.repository.postgresql import connection


@pytest.fixture(autouse=True)
async def clean_postgres():
    """Truncate all tables (except yoyo migrations) before each test."""

    q = """
        CREATE OR REPLACE FUNCTION truncate_tables() RETURNS void AS $$
        DECLARE
            statements CURSOR FOR
                SELECT tablename FROM pg_tables
                WHERE schemaname = 'public'
                    and tablename not like '%yoyo%'
                    and tablename not like 'user_roles';
        BEGIN
            FOR stmt IN statements LOOP
                EXECUTE 'TRUNCATE TABLE ' || quote_ident(stmt.tablename) || ' CASCADE;';
            END LOOP;
        END;
        $$ LANGUAGE plpgsql;
    """

    async with connection.get_connection(return_pool=True) as pool:
        async with connection.acquire_connection(pool) as cursor:
            await cursor.execute(q)
            await cursor.execute("select truncate_tables();")

    yield

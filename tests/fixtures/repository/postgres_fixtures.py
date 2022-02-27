import pytest

from app.internal.repository.postgresql import connection


@pytest.fixture(autouse=True)
async def _clean_postgres():
    """Deleting database values before each test."""
    await clean_postgres()


async def clean_postgres():
    """Truncate all tables (except yoyo migrations) before each test."""
    query = """
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
    async with connection.get_connection(testing=True) as cursor:
        await cursor.execute(query)
        await cursor.execute("select truncate_tables();")

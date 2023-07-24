from app.internal.repository.postgresql.connection import acquire_connection


async def test_connection(get_connection):
    async with acquire_connection(get_connection) as cursor:
        await cursor.execute("SELECT current_database();")
        response = await cursor.fetchone()

    assert dict(response)["current_database"].startswith("test_")

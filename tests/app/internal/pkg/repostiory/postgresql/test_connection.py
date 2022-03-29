from app.internal.repository.postgresql.connection import get_connection


async def test_connection():
    async with get_connection() as cursor:
        await cursor.execute("SELECT 'TEST_CONNECTION' as response")
        response = await cursor.fetchone()

    assert dict(response) == {"response": "TEST_CONNECTION"}

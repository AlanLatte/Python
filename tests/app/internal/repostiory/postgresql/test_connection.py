from app.internal.repository.postgresql.connection import get_connection


async def test_connection():
    async with get_connection() as cursor:
        await cursor.execute("SELECT current_database();")
        response = await cursor.fetchone()
    assert dict(response)["current_database"].startswith("test_")

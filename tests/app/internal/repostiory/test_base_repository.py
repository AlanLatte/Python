import pytest

from app.pkg.connectors.connector import BaseConnector


@pytest.mark.correct
async def test_raising_not_implemented_connection():
    connect = BaseConnector()

    with pytest.raises(NotImplementedError):
        await connect.get_connect()


@pytest.mark.correct
async def test_raising_not_implemented_close_connection():
    connect = BaseConnector()

    with pytest.raises(NotImplementedError):
        await connect.close()

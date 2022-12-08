import pytest
from app.pkg.connectors.base_connector import BaseConnector


async def test_raising_not_implemented():
    connect = BaseConnector()

    with pytest.raises(NotImplementedError):
        connect.get_dsn()

    with pytest.raises(AttributeError):
        async with connect.get_connect():
            ...

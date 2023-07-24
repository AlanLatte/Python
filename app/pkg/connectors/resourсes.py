from dependency_injector import resources

from app.pkg.connectors.connector import BaseConnector


__all__ = ["AsyncResource"]


class AsyncResource(resources.AsyncResource):
    async def init(self, connector: BaseConnector, *args, **kwargs):
        return await connector.get_connect(*args, **kwargs)

    async def shutdown(self, connection: BaseConnector):
        await connection.close()

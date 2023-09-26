"""``on_startup`` function will be called when server trying to start."""


async def on_startup() -> None:
    """Run code on server startup.

    Warnings:
        **Don't use this function for insert default data in database.
        For this action, we have scripts/migrate.py.**

    Returns:
        None
    """


async def on_shutdown() -> None:
    """Run code on server shutdown. Use this function for close all
    connections, etc.

    Returns:
        None
    """

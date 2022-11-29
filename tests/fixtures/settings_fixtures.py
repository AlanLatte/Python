import pytest

from app.configuration import __containers__
from app.pkg.settings.settings import get_settings

_settings = get_settings("../../.env")


@pytest.fixture()
async def settings(wire):
    _settings.POSTGRES_DATABASE_NAME = f"test_{_settings.POSTGRES_DATABASE_NAME}"
    return _settings


@pytest.fixture(autouse=True)
async def wire():
    __containers__.wire_packages(pkg_name=__name__)

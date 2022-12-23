import pytest

from app.internal.repository.repository import Repository
from app.pkg.models.base import Model


async def test_abstract_methods_create():
    with pytest.raises(NotImplementedError):
        await Repository().create(cmd=Model)


async def test_abstract_methods_read():
    with pytest.raises(NotImplementedError):
        await Repository().read(query=Model)


async def test_abstract_methods_read_all():
    with pytest.raises(NotImplementedError):
        await Repository().read_all()


async def test_abstract_methods_update():
    with pytest.raises(NotImplementedError):
        await Repository().update(cmd=Model)


async def test_abstract_methods_delete():
    with pytest.raises(NotImplementedError):
        await Repository().delete(cmd=Model)

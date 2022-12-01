import pytest

from app.pkg.models.base import Model


async def test_notimplemented_error(user_role_repository):
    with pytest.raises(NotImplementedError):
        await user_role_repository.delete(cmd=Model)

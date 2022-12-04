import pytest


async def test_notimplemented_error(user_role_repository):
    with pytest.raises(NotImplementedError):
        await user_role_repository.read_all()

"""Test cases for :meth:`.UserRoleRepository.read_all()`."""

import pytest

from app.internal.repository.postgresql.user_roles import UserRoleRepository


async def test_notimplemented_error(user_role_repository: UserRoleRepository):
    with pytest.raises(NotImplementedError):
        await user_role_repository.read_all()

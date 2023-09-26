"""Test cases for :meth:`.UserRoleRepository.delete()`."""

import pytest

from app.internal.repository.postgresql.user_roles import UserRoleRepository
from app.pkg.models.base import Model


async def test_notimplemented_error(user_role_repository: UserRoleRepository):
    with pytest.raises(NotImplementedError):
        await user_role_repository.delete(cmd=Model)

"""Test cases for :meth:`.JWTRefreshTokenRepository.read_all()`."""

import pytest

from app.internal.repository.postgresql import JWTRefreshTokenRepository


async def test_not_implemented(refresh_token_repository: JWTRefreshTokenRepository):
    with pytest.raises(NotImplementedError):
        await refresh_token_repository.read_all()

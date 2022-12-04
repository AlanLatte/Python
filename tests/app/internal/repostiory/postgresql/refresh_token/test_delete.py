import pytest
from app.internal.routes.user import delete_user

from app.pkg import models
from app.pkg.models.exceptions.repository import UniqueViolation
from app.internal.repository.postgresql.refresh_tokens import JWTRefreshTokenRepository
from tests.fixtures.repository.postgresql.user import insert_first_user


# async def test_correct(
#     refresh_token_repository: JWTRefreshTokenRepository, insert_first_user: models.User
# ):
    # refresh_token_repository.delete(cmd=insert_first_user.migrate(models.COmmd))

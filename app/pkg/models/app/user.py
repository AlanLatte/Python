"""User model."""

from pydantic.fields import Field
from pydantic.types import PositiveInt

from app.pkg.models.base import BaseModel
from app.pkg.models.types import EncryptedSecretBytes
from app.pkg.models.app.user_role import UserRole, UserRoleFields

__all__ = [
    "User",
    "UserFields",
    "CreateUserCommand",
    "ReadUserByIdQuery",
    "ReadUserByUserNameQuery",
    "UpdateUserCommand",
    "DeleteUserCommand",
    "ChangeUserPasswordCommand",
]


class UserFields:
    """Fields for user model."""

    id = Field(description="User id.", example=2)
    username = Field(description="User Login", example="TestTest")
    password = Field(
        description="User password",
        example="strong password",
        min_length=6,
        max_length=100,
    )
    old_password = Field(
        description="Old user password.",
        example="strong password",
        min_length=6,
        max_length=100,
    )
    new_password = Field(
        description="New user password.",
        example="strong password",
        min_length=6,
        max_length=100,
    )
    role_name = UserRoleFields.role_name


class BaseUser(BaseModel):
    """Base model for user."""


class User(BaseUser):
    id: PositiveInt = UserFields.id
    username: str = UserFields.username
    password: EncryptedSecretBytes = UserFields.password
    role_name: UserRole = UserFields.role_name


# Commands.
class CreateUserCommand(BaseUser):
    username: str = UserFields.username
    password: EncryptedSecretBytes = UserFields.password
    role_name: UserRole = UserFields.role_name


class UpdateUserCommand(BaseUser):
    id: PositiveInt = UserFields.id
    username: str = UserFields.username
    password: EncryptedSecretBytes = UserFields.password
    role_name: UserRole = UserFields.role_name


class DeleteUserCommand(BaseUser):
    id: PositiveInt = UserFields.id


class ChangeUserPasswordCommand(BaseUser):
    id: PositiveInt = UserFields.id
    old_password: EncryptedSecretBytes = UserFields.old_password
    new_password: EncryptedSecretBytes = UserFields.new_password


# Query
class ReadUserByUserNameQuery(BaseUser):
    username: str = UserFields.username


class ReadUserByIdQuery(BaseUser):
    id: PositiveInt = UserFields.id

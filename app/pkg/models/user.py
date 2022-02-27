from pydantic.fields import Field
from pydantic.types import PositiveInt
from pydantic import EmailStr

from .base import BaseModel
from .types import EncryptedSecretBytes
from .user_role import UserRole, UserRoleFields

__all__ = [
    "User",
    "CreateUserCommand",
    "ReadUserByIdQuery",
    "ReadUserByEmailQuery",
    "UpdateUserCommand",
    "DeleteUserCommand",
    "ChangeUserPasswordCommand"
]


class UserFields:
    id = Field(description="User id.", example=2)
    email = Field(description="User email.", example="ivan.ivanov@example.com")
    password = Field(
        description="User password.",
        example="strong password",
        min_length=6,
        max_length=256,
    )
    old_password = Field(
        description="Old user password.",
        example="strong password",
        min_length=6,
        max_length=256,
    )
    new_password = Field(
        description="New user password.",
        example="strong password",
        min_length=6,
        max_length=256,
    )
    role_name = UserRoleFields.role_name


class BaseUser(BaseModel):
    """Base model for user."""


class User(BaseUser):
    id: PositiveInt = UserFields.id
    email: EmailStr = UserFields.email
    password: EncryptedSecretBytes = UserFields.password
    role_name: UserRole = UserFields.role_name


# Commands.
class CreateUserCommand(BaseUser):
    email: EmailStr = UserFields.email
    password: EncryptedSecretBytes
    role_name: UserRole = UserFields.role_name


class UpdateUserCommand(BaseUser):
    id: PositiveInt = UserFields.id
    email: EmailStr = UserFields.email
    password: EncryptedSecretBytes
    role_name: UserRole = UserFields.role_name


class DeleteUserCommand(BaseUser):
    id: PositiveInt = UserFields.id


class ChangeUserPasswordCommand(BaseUser):
    id: PositiveInt = UserFields.id
    old_password: EncryptedSecretBytes = UserFields.old_password
    new_password: EncryptedSecretBytes = UserFields.new_password


# Query
class ReadUserByEmailQuery(BaseUser):
    email: EmailStr = UserFields.email


class ReadUserByIdQuery(BaseUser):
    id: PositiveInt = UserFields.id

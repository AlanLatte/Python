from pydantic import Field

from app.pkg.models.base import BaseEnum, BaseModel

__all__ = ["UserRole", "CreateUserRoleCommand", "UserRoleFields"]


class BaseUserRole(BaseModel):
    """Base model for user."""


class UserRole(BaseEnum):
    USER = "user"


class UserRoleFields:
    role_name = Field(
        default=UserRole.USER.value,
        description="User role name.",
        example=UserRole.USER.value,
    )


class CreateUserRoleCommand(BaseUserRole):
    role_name: UserRole = UserRoleFields.role_name

"""Base business models.

All models **must** inherit from them.
"""
# ruff: noqa

from app.pkg.models.base.enum import BaseEnum
from app.pkg.models.base.exception import BaseAPIException
from app.pkg.models.base.model import BaseModel, Model

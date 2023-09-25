"""Base business models.

They *must* inherit all models.
"""

from app.pkg.models.base.enum import BaseEnum
from app.pkg.models.base.exception import BaseAPIException
from app.pkg.models.base.model import BaseModel, Model

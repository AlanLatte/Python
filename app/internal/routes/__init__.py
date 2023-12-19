"""Global point for collected routers. __routes__ is a :class:`.Routes`
instance that contains all routers in your application.

Examples:
    After declaring all routers, you need to register them in your application::

        >>> from fastapi import FastAPI
        >>> app = FastAPI()
        >>> __routes__.register_routes(app=app)
"""

from fastapi import APIRouter

from app.pkg.models.core.routes import Routes
from app.pkg.models.exceptions import (
    city,
    contacts,
    country,
    direction,
    skill,
    skill_levels,
    partners,
)

__all__ = [
    "__routes__",
    "city_router",
    "contacts_router",
    "country_router",
    "direction_router",
    "skill_router",
    "skill_levels_router",
]

city_router = APIRouter(
    prefix="/country/city",
    tags=["City"],
    responses={
        **city.CityNotFound.generate_openapi(),
        **city.NoCityFoundForCountry.generate_openapi(),
        **city.DuplicateCityCode.generate_openapi(),
        **city.CountryAlreadyHasCities.generate_openapi(),
    },
)


contacts_router = APIRouter(
    prefix="/users/contacts",
    tags=["Contacts"],
    responses={
        **contacts.ContactsNotFound.generate_openapi(),
    },
)


country_router = APIRouter(
    prefix="/country",
    tags=["Country"],
    responses={
        **country.CountryNameAlreadyExists.generate_openapi(),
        **country.CountryCodeAlreadyExists.generate_openapi(),
        **country.CountryNotFound.generate_openapi(),
    },
)

direction_router = APIRouter(
    prefix="/skills/direction",
    tags=["Direction"],
    responses={
        **direction.DirectionNameAlreadyExists.generate_openapi(),
        **direction.DirectionNotFound.generate_openapi(),
    },
)


skill_router = APIRouter(
    prefix="/skills",
    tags=["Skills"],
    responses={
        **skill.SkillNameAlreadyExists.generate_openapi(),
        **skill.SkillNotFound.generate_openapi(),
    },
)


skill_levels_router = APIRouter(
    prefix="/skills/levels",
    tags=["Skill levels"],
    responses={
        **skill_levels.SkillLevelAlreadyExists.generate_openapi(),
    },
)

partners_router = APIRouter(
    prefix="/partners",
    tags=["Partner"],
    responses={
        **partners.PartnerNotFound.generate_openapi(),
    },
)


__routes__ = Routes(
    routers=(
        skill_router,
        skill_levels_router,
        direction_router,
        city_router,
        country_router,
        contacts_router,
        partners_router,
    ),
)

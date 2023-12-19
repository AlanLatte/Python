"""Service layer."""

from dependency_injector import containers, providers

from app.internal.repository import Repositories, postgresql
from app.internal.services.city import CityService
from app.internal.services.contacts import ContactsService
from app.internal.services.country import CountryService
from app.internal.services.direction import DirectionService
from app.internal.services.skill import SkillService
from app.internal.services.skill_levels import SkillLevelService
from app.internal.services.partners import PartnerService


class Services(containers.DeclarativeContainer):
    """Containers with services."""

    repositories: postgresql.Repositories = providers.Container(
        Repositories.postgres,
    )  # type: ignore

    skill_levels_service = providers.Factory(
        SkillLevelService,
        skill_level_repository=repositories.skill_levels_repository,
    )

    skill_service = providers.Factory(
        SkillService,
        skill_repository=repositories.skill_repository,
    )

    direction_service = providers.Factory(
        DirectionService,
        direction_repository=repositories.direction_repository,
    )

    city_service = providers.Factory(
        CityService,
        city_repository=repositories.city_repository,
    )

    country_service = providers.Factory(
        CountryService,
        country_repository=repositories.country_repository,
    )

    contacts_service = providers.Factory(
        ContactsService,
        contacts_repository=repositories.contacts_repository,
    )

    partner_service = providers.Factory(
        PartnerService,
        partner_repository=repositories.partner_repository,
    )

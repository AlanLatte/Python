"""All postgresql repositories are defined here."""

from dependency_injector import containers, providers

from app.internal.repository.postgresql.city import CityRepository
from app.internal.repository.postgresql.contacts import ContactsRepository
from app.internal.repository.postgresql.country import CountryRepository
from app.internal.repository.postgresql.direction import DirectionRepository
from app.internal.repository.postgresql.partners import PartnerRepository
from app.internal.repository.postgresql.skill import SkillRepository
from app.internal.repository.postgresql.skill_levels import SkillLevelRepository


class Repositories(containers.DeclarativeContainer):
    """Container for postgresql repositories."""

    skill_levels_repository = providers.Factory(SkillLevelRepository)
    skill_repository = providers.Factory(SkillRepository)
    direction_repository = providers.Factory(DirectionRepository)
    city_repository = providers.Factory(CityRepository)
    country_repository = providers.Factory(CountryRepository)
    contacts_repository = providers.Factory(ContactsRepository)
    partner_repository = providers.Factory(PartnerRepository)

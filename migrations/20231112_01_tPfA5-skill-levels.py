"""
skill_levels
"""

from yoyo import step

__depends__ = {}

steps = [
    step(
        """
            create table skill_levels(
                id serial primary key,
                level int not null unique check ( level >= 0 ),
                description text
            )
        """,
        """
            drop table if exists skill_levels cascade;
        """

    ),
]

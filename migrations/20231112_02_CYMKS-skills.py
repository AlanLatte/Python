"""
skills
"""

from yoyo import step

__depends__ = {'20231112_01_tPfA5-skill-levels'}

steps = [
    step(
        """
            create table skills(
                id serial primary key,
                name text not null unique
            );
        """,
        """
            drop table if exists skills;
        """
    )
]

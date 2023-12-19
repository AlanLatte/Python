"""
countries
"""

from yoyo import step

__depends__ = {'20231112_01_tPfA5-skill-levels'}

steps = [
    step(
        """
            create table countries(
                id serial primary key,
                name text not null unique,
                code text not null unique
            );
        """,
        """
            drop table if exists countries cascade;
        """
    )
]

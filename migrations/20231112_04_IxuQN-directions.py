"""
directions
"""

from yoyo import step

__depends__ = {'20231112_02_CYMKS-skills'}

steps = [
    step(
        """
            create table directions(
                id serial primary key,
                name text not null unique
            );
        """,
        """
            drop table if exists directions cascade ;
        """
    )
]

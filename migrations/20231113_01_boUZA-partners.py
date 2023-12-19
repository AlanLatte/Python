"""
partners
"""

from yoyo import step

__depends__ = {}

steps = [
    step(
        """
            create table partners(
                id serial primary key,
                name text not null unique,
                token text not null unique
            )
        """,
        """
            drop table if exists partners cascade;
        """,
    )
]

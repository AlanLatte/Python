"""
create user_roles table
"""

from yoyo import step

__depends__ = {}

steps = [
    step(
        """
            create table if not exists user_roles(
                id serial primary key,
                role_name text unique
            );
        """,
        """
            drop table if exists user_roles;
        """,
    )
]

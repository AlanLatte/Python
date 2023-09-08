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
                role_name text unique,
                
                check ( length(role_name) > 0 )
            );
        """,
        """
            drop table if exists user_roles;
        """,
    )
]

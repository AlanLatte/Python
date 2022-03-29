"""
create users table
"""

from yoyo import step

__depends__ = {"20220227_02_SEvNK-create-user-roles-table"}

steps = [
    step(
        """
            create table users(
                id serial primary key,
                email text unique not null,
                password bytea not null,
                role_name int references user_roles(id)
            )
        """,
        """
            drop table if exists users; 
        """
    )
]

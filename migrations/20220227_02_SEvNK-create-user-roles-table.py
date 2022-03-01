"""
create user_roles table
"""

from yoyo import step

__depends__ = {'20220227_02_SEvNK-create-user-roles-table'}

steps = [
    step(
        """
            create table user_roles(
                id serial primary key,
                role_name text unique
            )
        """,
        """
            drop table if exists user_roles;
        """
    )
]
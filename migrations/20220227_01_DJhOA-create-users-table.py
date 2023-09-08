"""
create users table
"""

from yoyo import step

__depends__ = {"20220227_02_SEvNK-create-user-roles-table"}

steps = [
    step(
        """
            create table if not exists users(
                id serial primary key,
                username text unique not null,
                password bytea not null,
                role_id int references user_roles(id) not null,
                password_updated_at timestamp default now() not null,
                
                check ( length(username) > 0 ),
                check ( length(password) > 0 ),
                check ( password_updated_at <= now() )
            )
        """,
        """
            drop table if exists users; 
        """,
    )
]

"""
create refresh tokens table
"""

from yoyo import step

__depends__ = {"20220227_01_DJhOA-create-users-table"}

steps = [
    step(
        """
            create table if not exists refresh_tokens(
                id serial primary key, 
                user_id int references users(id),
                refresh_token text not null unique,
                fingerprint text not null,
                constraint all_value_in_row_must_be_unique unique (
                    user_id, refresh_token, fingerprint
                )
            );
        """,
        """
            drop table if exists refresh_tokens cascade;
        """,
    )
]

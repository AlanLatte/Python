"""
contacts
"""

from yoyo import step

__depends__ = {'20231112_01_tPfA5-skill-levels', '20231113_01_boUZA-partners'}

steps = [
    step(
        """
            create table contacts(
                id serial primary key,
                token text unique not null,
                email text unique not null,
                telegram_username text not null unique,
                telegram_user_id bigint not null unique
            )
        """,
        """
            drop table if exists contacts cascade;
        """
    ),
    step(
        """
            alter table contacts
                alter column email drop not null;
        """,
        """
            alter table contacts
                alter column email set not null;
        """
    ),
    step(
        """
            alter table contacts
                alter column telegram_username drop not null;
        """,
        """
            alter table contacts
                alter column telegram_username set not null;
        """
    ),
    step(
        """
            alter table contacts
                add column partner_id int references partners(id);
        """,
        """
            alter table contacts
                drop column if exists partner_id;
        """
    )
]

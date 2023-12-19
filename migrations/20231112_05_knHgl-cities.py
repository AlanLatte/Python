"""
cities
"""

from yoyo import step

__depends__ = {'20231112_10_wPUeW-countries'}

steps = [
    step(
        """
            create table cities(
                id serial primary key,
                country_id int not null references countries,
                name text not null unique,
                code text not null unique,
                
                constraint unique_country_and_city_code unique (country_id, code)
            );
        """,
        """
            drop table if exists cities cascade;
        """
    )
]

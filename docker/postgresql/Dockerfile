FROM postgres:13.1

RUN apt-get update && \
    apt-get install -y --no-install-recommends dos2unix

ADD ./scripts/init.postgres.sh /docker-entrypoint-initdb.d/init-db.sh

RUN dos2unix /docker-entrypoint-initdb.d/init-db.sh

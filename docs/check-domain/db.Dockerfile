FROM mysql

ENV MYSQL_ROOT_PASSWORD=777
ENV MYSQL_DATABASE='check-domain'

COPY ./db_init /docker-entrypoint-initdb.d

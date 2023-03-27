FROM postgres:15.2

WORKDIR /tmp

COPY db_setup.sql /docker-entrypoint-initdb.d/

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y postgis

EXPOSE 5432

ENTRYPOINT [ "docker-entrypoint.sh" ]

CMD [ "postgres" ]

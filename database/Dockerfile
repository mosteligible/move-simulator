FROM mysql:8.0.31-debian

WORKDIR /tmp

COPY db_setup.sql /docker-entrypoint-initdb.d

RUN apt-get update && \
    apt-get upgrade -y

EXPOSE 3306
ENTRYPOINT [ "/usr/local/bin/docker-entrypoint.sh" ]
CMD [ "mysqld" ]

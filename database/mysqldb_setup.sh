#!/usr/bin/bash

export $(cat db.env)

if [[ -z "$PGRES_USERNAME" || \
      -z "$MYSQL_USER_PASSWORD" || \
      -z "$MYSQL_DB_NAME" || \
      -z "$MYSQL_USER_TABLE_NAME" || \
      -z "$MYSQL_ROUTE_TABLE_NAME" || \
      -z "$MYSQL_INITDB_ROOT_USERNAME" || \
      -z "$MYSQL_ROOT_PASSWORD" ]]; then
    echo ">> Environment variables
    PGRES_USERNAME
    PGRES_USER_PASSWORD
    POSTGRES_DB
    PGRES_USER_TABLE_NAME
    PGRES_ROUTE_TABLE_NAME
    POSTGRES_USER
    POSTGRES_PASSWORD
    must be set before running this target."
    exit 1
fi

echo ">> Database environment variables exported..."

echo ">> Generating db_setup.sql file..."

echo \
"CREATE USER $PGRES_USERNAME WITH PASSWORD '$PGRES_USER_PASSWORD';
CREATE DATABASE $POSTGRES_DB;

GRANT ALL PRIVILEGES ON DATABASE $POSTGRES_DB TO $PGRES_USERNAME;

\c $POSTGRES_DB;

CREATE TABLE IF NOT EXISTS $PGRES_USER_TABLE_NAME (
    id varchar(50) NOT NULL,
    username varchar(50) NOT NULL UNIQUE,
    email varchar(250) NOT NULL UNIQUE,
    password varchar(255) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS $PGRES_ROUTE_TABLE_NAME (
    id varchar(50) NOT NULL,
    username varchar(50) NOT NULL,
    userid varchar(50) NOT NULL,
    last_position geography NOT NULL,
    distance_covered int NOT NULL,
    start_street_address varchar(250) NOT NULL,
    start_city varchar(250) NOT NULL,
    start_country varchar(50) NOT NULL,
    end_street_address varchar(250) NOT NULL,
    end_city varchar(250) NOT NULL,
    end_country varchar(50) NOT NULL,
    start_position geography NOT NULL,
    end_position geography NOT NULL,
    last_position geography NOT NULL,
    route_coordinates json NOT NULL,
    PRIMARY KEY (id)
);

GRANT ALL ON ALL TABLES IN SCHEMA public TO $PGRES_USERNAME;
" > ./database/db_setup.sql

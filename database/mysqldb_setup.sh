#!/usr/bin/bash

export $(cat db.env)

if [[ -z "$MYSQL_USERNAME" || \
      -z "$MYSQL_USER_PASSWORD" || \
      -z "$MYSQL_DB_NAME" || \
      -z "$MYSQL_USER_TABLE_NAME" || \
      -z "$MYSQL_ROUTE_TABLE_NAME" || \
      -z "$MYSQL_INITDB_ROOT_USERNAME" || \
      -z "$MYSQL_ROOT_PASSWORD" ]]; then
    echo ">> Environment variables
    MYSQL_USERNAME
    MYSQL_USER_PASSWORD
    MYSQL_DB_NAME
    MYSQL_USER_TABLE_NAME
    MYSQL_ROUTE_TABLE_NAME
    MYSQL_INITDB_ROOT_USERNAME
    MYSQL_ROOT_PASSWORD
    must be set before running this target."
    exit 1
fi

echo ">> Database environment variables exported..."

echo ">> Generating db_setup.sql file..."

echo \
"CREATE DATABASE IF NOT EXISTS $MYSQL_DB_NAME;
USE $MYSQL_DB_NAME;
CREATE TABLE IF NOT EXISTS $MYSQL_USER_TABLE_NAME (
    id varchar(50) NOT NULL,
    username varchar(50) NOT NULL,
    email varchar(250) NOT NULL,
    password varchar(255) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS $MYSQL_ROUTE_TABLE_NAME (
    id varchar(50) NOT NULL,
    username varchar(50) NOT NULL,
    userid varchar(50) NOT NULL,
    last_position point NOT NULL,
    start_position point NOT NULL,
    end_position point NOT NULL,
    route_coordinates json NOT NULL,
    PRIMARY KEY (id)
);

CREATE USER '$MYSQL_USERNAME'@'%' IDENTIFIED BY '$MYSQL_USER_PASSWORD';
GRANT ALL ON $MYSQL_DB_NAME.* TO '$MYSQL_USERNAME'@'%';
" > ./database/db_setup.sql

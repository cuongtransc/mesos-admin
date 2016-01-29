#!/bin/bash

BASE_DIR=$(dirname ${0})
BASE_DIR=$(readlink -f "${BASE_DIR}")

source ${BASE_DIR}/env_get_project_env.sh
PG_CONTAINER_NAME=${PROJECT_NAME}_postgres_1

# get postgres authentication
source ${BASE_DIR}/env_postgres_auth.sh

if [ -z "$1" ]; then
    echo "Usage: ./postgres_backup.sh file_backup [db-name]"
    exit 1
fi

FILE_BACKUP=$1
FILE_BACKUP=$(readlink -f "${FILE_BACKUP}")

# overwrite postgres parameters
if [ ! -z "$2" ]; then
    PG_DATABASE=$2
fi

# run restore
DATE1=$(date -u +"%s")

docker run -i --rm \
    --link ${PG_CONTAINER_NAME}:postgres \
    -v ${FILE_BACKUP}:/tmp/pg_dump.backup \
    -e PG_PASSWORD=${PG_PASSWORD} \
    -e PG_USER=${PG_USER} \
    -e PG_DATABASE=${PG_DATABASE} \
    postgres:9.4 \
    bash -c 'export PGPASSWORD=${PG_PASSWORD}; exec pg_restore -h "$POSTGRES_PORT_5432_TCP_ADDR" -p "$POSTGRES_PORT_5432_TCP_PORT" -U ${PG_USER} -d ${PG_DATABASE} -Fc -v /tmp/pg_dump.backup'

DATE2=$(date -u +"%s")
DIFF=$(($DATE2-$DATE1))
echo "Finished in $(($DIFF / 60)) minutes and $(($DIFF % 60)) seconds."

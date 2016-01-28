#!/bin/bash

BASE_DIR=$(dirname ${0})
BASE_DIR=$(readlink -f "${BASE_DIR}")

source ${BASE_DIR}/env_get_project_env.sh
PG_CONTAINER_NAME=${PROJECT_NAME}_postgres_1

# get postgres authentication
source ${BASE_DIR}/env_postgres_auth.sh

PG_HOST=`docker inspect --format '{{.NetworkSettings.IPAddress}}'  ${PG_CONTAINER_NAME}`

PGPASSWORD=${PG_PASSWORD} psql -h ${PG_HOST} -U ${PG_USER} -d ${PG_DATABASE}

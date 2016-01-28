#!/bin/bash

BASE_DIR=$(dirname ${0})
BASE_DIR=$(readlink -f "${BASE_DIR}")

source ${BASE_DIR}/env_get_project_env.sh
PG_CONTAINER_NAME=${PROJECT_NAME}_postgres_1

BACKUP_DIR=${BASE_DIR}/postgres_dump
BACKUP_CLEANER_LOG=${BASE_DIR}/logs/backup_cleaner.log
KEEP_N_VERSION=10

# get postgres authentication
source ${BASE_DIR}/env_postgres_auth.sh

# overwrite postgres parameters
if [ ! -z "$1" ]; then
    PG_DATABASE=$1
fi

# run backup
DATE1=$(date -u +"%s")

DATE_BACKUP=`date +%Y-%m-%d"_"%H_%M_%S`

docker run -i --rm \
    --link ${PG_CONTAINER_NAME}:postgres \
    -v ${BACKUP_DIR}:/tmp/ \
    -e PG_PASSWORD=${PG_PASSWORD} \
    -e PG_USER=${PG_USER} \
    -e PG_DATABASE=${PG_DATABASE} \
    -e DATE_BACKUP=${DATE_BACKUP} \
    postgres:9.4 \
    bash -c 'export PGPASSWORD=${PG_PASSWORD}; exec pg_dump -h "${POSTGRES_PORT_5432_TCP_ADDR}" -p "${POSTGRES_PORT_5432_TCP_PORT}" -U ${PG_USER} -Fc -v -d ${PG_DATABASE} > /tmp/${PG_DATABASE}_${DATE_BACKUP}.backup'

echo ${DATE_BACKUP} Delete old backup | tee -a ${BACKUP_CLEANER_LOG}
ls -d -t1 ${BACKUP_DIR}/${PG_DATABASE}_*.backup | tail -n +$((${KEEP_N_VERSION} + 1)) | xargs -r rm -rfv 2>> ${BACKUP_CLEANER_LOG}

DATE2=$(date -u +"%s")
DIFF=$(($DATE2-$DATE1))
echo "Finished in $(($DIFF / 60)) minutes and $(($DIFF % 60)) seconds."

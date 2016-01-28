#!/bin/bash

BASE_DIR=$(dirname ${0})
BASE_DIR=$(readlink -f "${BASE_DIR}")

bash ${BASE_DIR}/postgres_backup.sh
bash ${BASE_DIR}/postgres_backup.sh olbiusolap


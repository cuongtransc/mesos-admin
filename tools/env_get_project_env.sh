#!/bin/bash


# get project path
PROJECT_DIR=`readlink -f ${0}`
PROJECT_DIR=`dirname ${PROJECT_DIR}`
PROJECT_DIR=`dirname ${PROJECT_DIR}`

PROJECT_DIR_NAME=`basename "${PROJECT_DIR}"`

DOCKER_STYLE_NAME=`echo "${PROJECT_DIR_NAME}" | sed 's/\(-\|_\|\s\)//g'`
PROJECT_NAME=${DOCKER_STYLE_NAME}

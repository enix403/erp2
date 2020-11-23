#!/bin/bash

SCRIPT=$(readlink -f "$0")
# Absolute path this script is in, thus /home/user/bin
SCRIPTPATH=$(dirname "$SCRIPT")

rsync \
    -av \
    --exclude="/salary/frontend/node_modules" \
    --exclude="/salary/frontend/dist" \
    --exclude="/env" \
    --exclude=".git" \
	--exclude="**/.gitignore"
    --exclude="**/__pycache__" \
    --exclude="**/package-lock.json" \
    --exclude="**/*.js.map" \
    --exclude="**/*.css.map" \
    --exclude="/storage/sessions/*" \
    --exclude="/salary/migrations" \
    --exclude="/bin" \
    --exclude="/run" \
    --exclude="/static" \
    --exclude="/base/.env" \
    --exclude="/act" \
    --delete \
    $SCRIPTPATH/ $1
# --exclude="salary/static/lib/@blueprintjs" \



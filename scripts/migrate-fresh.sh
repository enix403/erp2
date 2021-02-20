#!/bin/bash

# migrate salary zero
# delete all files in salary/migrations except __init__.py
# makemigrations salary
# migrate

ROOT=$(readlink -f $(dirname "$0")/..)

source $ROOT/config/environs/.hrcupdate.env
source $ROOT/act

echo "Flushing database..." 
echo "yes" | $ROOT/manage.py reset_db > /dev/null
echo "Flush complete"

echo "Starting fresh database migration..."
rm -rf $ROOT/migrations/$MIGRATIONS_SUBFOLDER/*
mkdir -p $ROOT/migrations/$MIGRATIONS_SUBFOLDER
touch $ROOT/migrations/$MIGRATIONS_SUBFOLDER/__init__.py
$ROOT/manage.py makemigrations salary
$ROOT/manage.py migrate
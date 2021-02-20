#!/bin/bash
ROOT=$(readlink -f $(dirname "$0")/..)
source $ROOT/act
$ROOT/manage.py makemigrations salary
$ROOT/manage.py migrate
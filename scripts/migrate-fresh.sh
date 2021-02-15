#!/bin/bash

# migrate salary zero
# delete all files in salary/migrations except __init__.py
# makemigrations salary
# migrate

. act
./t migrate salary zero
rm -rf salary/migrations/*
mkdir -p salary/migrations
touch salary/migrations/__init__.py
./t makemigrations salary
./t migrate
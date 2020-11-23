#!/bin/bash

SCRIPT=$(readlink -f "$0")
# Absolute path this script is in, thus /home/user/bin
SCRIPTPATH=$(dirname "$SCRIPT")

rsync \
	-av
	$SCRIPTPATH/.git $1



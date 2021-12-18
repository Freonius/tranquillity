#!/bin/sh
SCRIPTPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
sh ${SCRIPTPATH}/../../src/python/shell/build-wheel.sh
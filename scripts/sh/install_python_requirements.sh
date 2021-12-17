#!/bin/sh
SCRIPTPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
python -m pip install --compile -r ${SCRIPTPATH}/../../src/python/shell/requirements.txt
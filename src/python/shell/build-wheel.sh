#!/bin/sh
SCRIPTPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
python ${SCRIPTPATH}/setup.py bdist --dist-dir ${SCRIPTPATH}/dist
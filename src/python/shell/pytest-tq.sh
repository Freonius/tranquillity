#!/bin/sh
SCRIPTPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
python -m pip install -r ${SCRIPTPATH}/../../../requirements-dev.txt
python -m pip install -r ${SCRIPTPATH}/requirements.txt
python -m pytest ${SCRIPTPATH}/test --cov=${SCRIPTPATH}/ --cov-report=xml:${SCRIPTPATH}/../../../coverage/shell.xml --cov-report=html:${SCRIPTPATH}/../../../coverage/shell
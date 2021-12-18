#!/bin/bash
SCRIPTPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
LOG_FILE=${SCRIPTPATH}/logs/setup.log

if [[ ! -d ${SCRIPTPATH}/logs ]]; then
    mkdir -p ${SCRIPTPATH}/logs
fi

function has_param() {
    local terms="$1"
    shift
    
    for term in $terms; do
        for arg; do
            if [[ $arg == "$term" ]]; then
                echo 1
                exit
            fi
        done
    done
    echo 0
}

function log() {
    local msg="$1"
    echo "$(date) :: ${msg}" >> $LOG_FILE
    echo "$(date) :: ${msg}"
}

RUN_PYTHON=$(has_param "py python" "$@")
RUN_DART=$(has_param "dart flutter" "$@")
RUN_REACT=$(has_param "javascript js typescript ts react" "$@")

RUN_TESTS=$(has_param "--test --tests -t" "$@")
RUN_LINT=$(has_param "--lint -l" "$@")
RUN_BUILD=$(has_param "--build -b" "$@")
RUN_INSTALL=$(has_param "--install -i" "$@")
RUN_DOCKER=$(has_param "--docker -d" "$@")
RUN_PUBLISH=$(has_param "--publish -p" "$@")
RUN_EDITABLE=$(has_param "--editable -e" "$@")
RUN_MODULES=$(has_param "--module --modules -m" "$@")

log "Running tranquillity installer"
log "linter=${RUN_LINT}"
log "tests=${RUN_TESTS}"
log "build=${RUN_BUILD}"
log "install=${RUN_INSTALL}"
log "editable=${RUN_EDITABLE}"
log "docker=${RUN_DOCKER}"
log "publish=${RUN_PUBLISH}"

PYTHON_FOLDERS=(
    "enums"
    "exceptions"
    "utils"
    "shell"
    "path"
    "files"
    "settings"
    "logger"
    "regexes"
    "connections"
    "query"
    "data"
    "html"
    "email"
    "queue"
    "schedulable"
    "api"
    "_"
)

if [[ ${RUN_PYTHON} -eq 1 ]]; then
    log "Running python installers"
    log "Checking if python is installed"
    PYTHON_CMD="python"
    ${PYTHON_CMD} -V >> /dev/null 2>&1
    if [[ $? -ne 0 ]]; then
        log "Checking with python3"
        PYTHON_CMD="python3"
        ${PYTHON_CMD} -V >> /dev/null 2>&1
        if [[ $? -ne 0 ]]; then
            log "Pyhton is not installed"
            exit 1
        else
            log "OK"
        fi
    else
        log "OK"
    fi
    if [[ ${RUN_TESTS} -eq 1 || ${RUN_LINT} -eq 1 || ${RUN_PUBLISH} -eq 1 ]]; then
        ${PYTHON_CMD} -m pip install -r ${SCRIPTPATH}/requirements-dev.txt
    fi
    if [[ ${RUN_LINT} -eq 1 ]]; then
        if [[ ! -d ${SCRIPTPATH}/lint ]]; then
            mkdir -p ${SCRIPTPATH}/lint
        fi
    fi
    for fld in ${PYTHON_FOLDERS[@]}; do
        if [[ ${RUN_MODULES} -eq 1 && $(has_param "${fld}" "$@") -eq 0 ]]; then
            log "Skipping ${fld}"
            continue
        fi
        log "====================================="
        log "== Running for folder ${fld} =="
        log "====================================="
        FULL_PY_FOLDER="${SCRIPTPATH}/src/python/${fld}"
        if [[ ${RUN_LINT} -eq 1 ]]; then
            if [[ ${fld} == "_" ]]; then
                log "Skipping _"
            else
                log "Running linter for folder ${fld}"
                if [[ -f ${SCRIPTPATH}/lint/${fld}.json ]]; then
                    rm -f ${SCRIPTPATH}/lint/${fld}.json
                fi
                touch ${SCRIPTPATH}/lint/${fld}.json
                ${PYTHON_CMD} -m pylint ${FULL_PY_FOLDER}/tranquillity/${fld}/ --reports=y --output-format=json:lint/${fld}.json,colorized
                if [[ $? -ne 0 ]]; then
                    log "ERROR :: linting failed for folder ${fld}"
                    exit 1
                fi
                ${PYTHON_CMD} -m mypy ${FULL_PY_FOLDER}/tranquillity/${fld}/
                if [[ $? -ne 0 ]]; then
                    log "ERROR :: linting failed for folder ${fld}"
                    exit 1
                fi
            fi
        fi
        if [[ ${RUN_TESTS} -eq 1 ]]; then
            log "Running tests for folder ${fld}"
            ${PYTHON_CMD} -m pip install -r ${FULL_PY_FOLDER}/requirements.txt
            if [[ $? -ne 0 ]]; then
                log "ERROR :: Could not install requirements for folder ${fld}"
                exit 1
            fi
            ${PYTHON_CMD} -m pytest ${FULL_PY_FOLDER}/test --cov=${FULL_PY_FOLDER}/tranquillity/${fld}/ --cov-report=xml:${SCRIPTPATH}/coverage/${fld}.xml --cov-report=html:${SCRIPTPATH}/coverage/${fld}
            if [[ $? -ne 0 ]]; then
                log "ERROR :: tests failed for folder ${fld}"
                exit 1
            fi
        fi
        if [[ ${RUN_BUILD} -eq 1 ]]; then
            log "Running build for folder ${fld}"
            ${PYTHON_CMD} ${FULL_PY_FOLDER}/setup.py bdist --dist-dir ${FULL_PY_FOLDER}/dist
            if [[ $? -ne 0 ]]; then
                log "ERROR :: build failed for folder ${fld}"
                exit 1
            fi
        fi
        if [[ ${RUN_INSTALL} -eq 1 ]]; then
            log "Running install for folder ${fld}"
            # ${PYTHON_CMD} -m pip install --compile -r ${FULL_PY_FOLDER}/requirements.txt
            EDITABLE_FLAG=""
            if [[ ${RUN_EDITABLE} -eq 1 ]]; then
                EDITABLE_FLAG="-e"
            fi
            ${PYTHON_CMD} -m pip install --compile ${EDITABLE_FLAG} ${FULL_PY_FOLDER}/.
            if [[ $? -ne 0 ]]; then
                log "ERROR :: install failed for folder ${fld}"
                exit 1
            fi
        fi
        if [[ ${RUN_PUBLISH} -eq 1 ]]; then
            log "Running publish for folder ${fld}"
            # TODO: Upload with twine
            if [[ $? -ne 0 ]]; then
                log "ERROR :: publish failed for folder ${fld}"
                exit 1
            fi
        fi
    done
    if [[ ${RUN_DOCKER} -eq 1 ]]; then
        log "Running docker"
        # TODO: docker buil
    fi
fi

if [[ ${RUN_DART} -eq 1 ]]; then
    echo "Dart"
fi

if [[ ${RUN_REACT} -eq 1 ]]; then
    echo "React"
fi

exit 0
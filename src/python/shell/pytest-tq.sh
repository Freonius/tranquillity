#!/bin/sh
# python -m pip install -r ./requirements-dev.txt
python -m pytest ./test --cov --cov-report html:pytest_coverage
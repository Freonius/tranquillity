@ECHO OFF
python -m pip install -r %~dp0..\..\..\requirements-dev.txt
python -m pip install -r %~dp0requirements.txt
python -m pytest %~dp0test --cov=%~dp0 --ignore=%~dp0setup.py --cov-report=xml:%~dp0..\..\..\coverage\shell.xml --cov-report=html:%~dp0..\..\..\coverage\shell
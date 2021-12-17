@ECHO OFF
python -m pip install --compile -r %~dp0requirements.txt
python -m pip install --compile %~dp0.
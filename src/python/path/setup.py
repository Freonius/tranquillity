from os.path import abspath, sep, isfile
from os import getenv
from typing import List
from pathlib import Path
from setuptools import setup, find_packages
from dotenv import load_dotenv

fld: str = str(Path(abspath(__file__)).parent) + sep

load_dotenv(fld + '..' + sep + '..' + sep + '..' + sep + '.env')
_version = getenv('TQ_VERSION', '0.1.0')

reqs: List[str] = []
if isfile(fld + 'requirements.txt'):
    reqs = list(filter(lambda x: x != '' and not x.startswith(
        '#'), list(map(str.strip, open(fld + 'requirements.txt', 'r').readlines()))))

setup(name='tranquillity.path', version=_version, packages=find_packages(exclude=['test', ],), install_requires=reqs,
      author='Federico Pirani',
      description='Tranquillity path.')

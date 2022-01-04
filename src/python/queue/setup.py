from os.path import abspath, sep, isfile
from os import getenv
from typing import List
from pathlib import Path
from setuptools import setup, find_packages
from dotenv import load_dotenv

fld: str = str(Path(abspath(__file__)).parent) + sep

load_dotenv(fld + '..' + sep + '..' + sep + '..' + sep + '.env')

readme_path = fld + '..' + sep + '..' + sep + '..' + sep + 'README.md'

ld = ''
if isfile(readme_path):
    with open(readme_path, encoding='utf-8', mode='r') as _f:
        ld = _f.read()

_version = getenv('TQ_VERSION', '0.1.0')

reqs: List[str] = []
if isfile(fld + 'requirements.txt'):
    reqs = list(filter(lambda x: x != '' and not x.startswith(
        '#'), list(map(str.strip, open(fld + 'requirements.txt', 'r').readlines()))))

for _i in range(len(reqs)):
    if reqs[_i].startswith('tranquillity'):
        reqs[_i] = reqs[_i].replace('{TQ_VER}', _version)

setup(name='tranquillity.queue', version=_version, packages=find_packages(exclude=['test', ],), install_requires=reqs,
      author='Federico Pirani',
      description='Tranquillity queue.', long_description=ld,
      long_description_content_type='text/markdown',
      project_urls={
    'Source': 'https://github.com/Freonius/tranquillity',
    'Tracker': 'https://github.com/Freonius/tranquillity/issues',
},
    url='https://github.com/Freonius/tranquillity',)

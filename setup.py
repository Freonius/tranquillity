from os.path import abspath, sep, isfile
from os import getenv
from pathlib import Path
from dotenv import load_dotenv
import re
import subprocess
from setuptools import find_packages, setup
from setuptools.command.install import install
from setuptools.command.develop import develop

__requires__ = ['pipenv']

base_dir: str = str(Path(abspath(__file__)).parent) + sep

load_dotenv(base_dir + '.env')

__version__ = getenv('TQ_VERSION', '0.1.0') # Just in case

PACKAGE_NAME = 'tranquillity'
SOURCE_DIRECTORY = 'src'
SOURCE_PACKAGE_REGEX = re.compile(rf'^{SOURCE_DIRECTORY}')

source_packages = find_packages(
    include=[SOURCE_DIRECTORY, f'{SOURCE_DIRECTORY}.*'], exclude=['tests'])
proj_packages = [SOURCE_PACKAGE_REGEX.sub(
    PACKAGE_NAME, name) for name in source_packages]



readme_path = base_dir + 'README.md'

long_description: str = ''
if isfile(readme_path):
    with open(readme_path, encoding='utf-8', mode='r') as _f:
        long_description = _f.read()



pipenv_command = ['pipenv', 'install', '--deploy', '--system']
pipenv_command_dev = ['pipenv', 'install', '--dev', '--deploy', '--system']

class PostDevelopCommand(develop):
    """Post-installation for development mode."""
    def run(self):
        subprocess.check_call(pipenv_command_dev)
        develop.run(self)

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        subprocess.check_call(pipenv_command)
        install.run(self)

setup(
    name=PACKAGE_NAME,
    packages=proj_packages,
    package_dir={PACKAGE_NAME: SOURCE_DIRECTORY},
    use_scm_version = {
        "root": ".",
        "relative_to": __file__,
        # "local_scheme": "node-and-timestamp"
    },
    version=__version__,
    setup_requires=['setuptools_scm'],
    cmdclass={
        'develop': PostDevelopCommand,
        'install': PostInstallCommand,
    },
    author='Federico Pirani',
    description='Tranquillity exceptions.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    project_urls={
        'Source': 'https://github.com/Freonius/tranquillity',
        'Tracker': 'https://github.com/Freonius/tranquillity/issues',
    },
    url='https://github.com/Freonius/tranquillity',
)
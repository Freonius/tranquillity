from setuptools import setup, find_packages

setup(name='tranquillity.settings',
      version='0.1.0', packages=find_packages(),
      install_requires=[
          'spring-config-client==0.2',
          'PyYAML==5.4.1',
          'configobj==5.0.6',
          'requests==2.25.1',
          # Tranquillity
          'tranquillity.exceptions>=0.1.0',
          'tranquillity.utils>=0.1.0'
      ],
      author='Federico Pirani',
      description='Tranquillity exceptions.')

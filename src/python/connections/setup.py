from setuptools import setup, find_packages

setup(name='tranquillity.connections',
      version='0.1.0', packages=find_packages(),
      install_requires=[
          'CouchDB==1.2',
          'elasticsearch==7.13.1',
          'elasticsearch[async]==7.13.1',
          'pymongo==3.11.4',
          'pika==1.2.0',
          'hazelcast-python-client==4.2',
          'kafka-python==2.0.2',
      ],
      author='Federico Pirani',
      description='Tranquillity connections.')

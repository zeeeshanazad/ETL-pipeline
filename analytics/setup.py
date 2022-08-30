
# Always prefer setuptools over distutils
from setuptools import setup, find_packages

setup(name='task',
      description='Data engineer task',
      version='1.0',
      author='zeeshan',
      install_requires=[
          'pandas==1.4.3',
          'geopy==2.2.0',
      ],
      packages=find_packages())

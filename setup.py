import os
from setuptools import setup

setup(name='lavoro-library',
      version=os.environ["CI_PIPELINE_CREATED_AT"].replace("-", ".")
      description='Shared library for Lavoro services',
      url='https://gitlab.com/rprojekt1/lavoro-library/',
      author='Lavoro Team',
      author_email='marko.bolt@fer.hr',
      license='MIT',
      packages=['lavoro_library'],
      zip_safe=False)
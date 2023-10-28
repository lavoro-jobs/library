import os
from setuptools import setup

setup(name='lavoro-library',
      version=os.environ["CI_PIPELINE_IID"],
      long_description="Shared library for Lavoro services",
      description='Shared library for Lavoro services',
      url='https://gitlab.com/rprojekt1/lavoro-library/',
      author='Lavoro Team',
      author_email='marko.bolt@fer.hr',
      license='MIT',
      install_requires=['psycopg2-binary'],
      packages=['lavoro_library'],
      zip_safe=False)
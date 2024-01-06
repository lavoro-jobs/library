import os
from setuptools import setup, find_packages

setup(
    name="lavoro-library",
    version=os.environ["CI_PIPELINE_IID"],
    long_description="Shared library for Lavoro services",
    description="Shared library for Lavoro services",
    url="https://gitlab.com/rprojekt1/lavoro-library/",
    author="Lavoro Team",
    author_email="marko.bolt@fer.hr",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "pydantic[email]",
        "psycopg[binary]",
        "python-multipart",
        "jsonpickle",
        "pika",
        "fastapi",
        "fastapi-mail",
    ],
    zip_safe=False,
)

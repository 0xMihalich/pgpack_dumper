import shutil
from setuptools import (
    find_packages,
    setup,
)

shutil.rmtree("build", ignore_errors=True)
shutil.rmtree("pgpack.egg-info", ignore_errors=True)

with open(file="README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="pgpack_dumper",
    version="0.1.2.2",
    packages=find_packages(),
    author="0xMihalich",
    author_email="bayanmobile87@gmail.com",
    description=(
        "Library for read and write PGPack "
        "format between PostgreSQL and file."
    ),
    url="https://github.com/0xMihalich/pgpack_dumper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    zip_safe=False,
    package_data={
        "pgpack_dumper.queryes": ["*.sql"],
    },
    include_package_data=True,
)

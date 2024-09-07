"""Python setup.py for project_name package"""
import io
import os
import re
from setuptools import find_packages, setup


def read(*paths, **kwargs):
    # """Read the contents of a text file safely.
    # >>> read("project_name", "VERSION")
    # '0.1.0'
    # >>> read("README.md")
    # ...
    # """

    content = ""
    with io.open(
            os.path.join(os.path.dirname(__file__), *paths),
            encoding=kwargs.get("encoding", "utf8"),
    ) as open_file:
        content = open_file.read().strip()
    return content


install_requires = read('requirements.txt')
# version = read('VERSION')
version = os.environ.get('main_version')


PACKAGE_NAME = 'ems'
SOURCE_DIRECTORY = 'ems'
SOURCE_PACKAGE_REGEX = re.compile(rf'^{SOURCE_DIRECTORY}')

source_packages = find_packages(include=[SOURCE_DIRECTORY, f'{SOURCE_DIRECTORY}.*', 'dependency'], exclude=["tests", ".github","__pycache__"])
proj_packages = [SOURCE_PACKAGE_REGEX.sub(PACKAGE_NAME, name) for name in source_packages]

setup(
    name=PACKAGE_NAME,
    version=version,
    description=PACKAGE_NAME,
    # url="",
    # long_description=read("README.md"),
    # long_description_content_type="text/markdown",
    # author="",
    packages=proj_packages,
    package_dir={PACKAGE_NAME: SOURCE_DIRECTORY},
    install_requires=install_requires,
    entry_points={
        "console_scripts": ["ems = ems.main:main"]
    }
    # extras_require={"test": read_requirements("requirements-test.txt")},
)

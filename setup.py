import os
import re
from setuptools import setup, find_packages

thisdir = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(thisdir, "README.md"), mode="r") as f:
    LONG_DESCRIPTION = f.read()


def read(*parts):
    with open(os.path.join(thisdir, *parts), "r") as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name="maxpytest",
    version=find_version("maxpytest", "__init__.py"),
    url="https://github.com/garytyler/maxpytest",
    author="Gary Tyler",
    author_email="mail@garytyler.com",
    description="Command line utility for using the Pytest testing framework in 3ds Max",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    python_requires="~=2.7",
    install_requires=["pytest", "pipenv"],
    tests_require=["pytest", "pytest-mock", "pipenv", "tox", "pytest-cov"],
    packages=["maxpytest"],
    entry_points={"console_scripts": ["maxpytest=maxpytest.cli:main"]},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 2.7",
        "Intended Audience :: End Users/Desktop",
        "Environment :: Console",
        "Programming Language :: Python :: 2.7",
        "Framework :: Pytest",
        "Topic :: Games/Entertainment :: Simulation",
        "Topic :: Multimedia",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Multimedia :: Graphics :: 3D Modeling",
        "Topic :: Multimedia :: Graphics :: 3D Rendering",
        "Topic :: Software Development :: Testing",
        "License :: OSI Approved :: MIT License",
    ],
)

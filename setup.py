#!/usr/bin/env python
import os
from setuptools import find_packages
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

version = {}
with open(os.path.join(here, "matchms-extras", "__version__.py")) as f:
    exec(f.read(), version)

with open("README.md") as readme_file:
    readme = readme_file.read()

setup(
    name="matchms-extras",
    version=version["__version__"],
    description="Additional functionalities to be used with matchms",
    long_description=readme,
    author="Netherlands eScience Center",
    author_email="f.huber@esciencecenter.nl",
    url="https://github.com/matchms/matchms-extras",
    packages=find_packages(exclude=['*tests*']),
    include_package_data=True,
    license="Apache Software License 2.0",
    zip_safe=False,
    keywords=[
        "similarity measures",
        "mass spectrometry",
        "networking",
        "network analysis",
        "library search",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8"
    ],
    test_suite="tests",
    python_requires='>=3.7',
    install_requires=[
        "matchms",
        "community",
        "networkx",
    ],
    extras_require={"dev": ["bump2version",
                            "isort>=4.2.5,<5",
                            "prospector[with_pyroma]",
                            "pytest",
                            "pytest-cov",
                            "sphinx>=3.0.0,!=3.2.0,!=3.5.0,<4.0.0",
                            "sphinx_rtd_theme",
                            "sphinxcontrib-apidoc",
                            "yapf",],
                    "chemistry": ["rdkit >=2020.03.1"]},
)

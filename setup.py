"""Builds the package.
"""
import os
import sys
import pkg_resources
from setuptools import setup, find_packages


VERSION = "0.0.1"
DESCRIPTION = "Nextmining Forecasting"

setup(
    name="nextmining-forecasting",
    version=VERSION,
    description=DESCRIPTION,
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="unknown",
    # author_email="<dev@nextmining.com>",
    package_dir={"": "src"},
    # url="https://github.com/louiezzang/nextmining-forecasting",
    keywors=[
        "Temporal Fusion Transformer",
        "Forecast",
    ],
    packages=find_packages(where="src"),
    install_requires=[
        str(r)
        for r in pkg_resources.parse_requirements(
            open(os.path.join(os.path.dirname(__file__), "requirements.txt"))
        )
    ],
    python_requires=">=3.6",
    include_package_data=True,
)
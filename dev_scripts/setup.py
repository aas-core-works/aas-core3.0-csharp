"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""
import os

from setuptools import setup, find_packages

# pylint: disable=redefined-builtin

setup(
    name="aas-core3.0-csharp-dev-scripts",
    version="0.0.1",
    description="Provide scripts for development of aas-core3.0-csharp.",
    url="https://github.com/aas-core-works/aas-core3.0-csharp",
    author="Marko Ristin",
    author_email="marko@ristin.ch",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    license="License :: OSI Approved :: MIT License",
    keywords="asset administration shell code generation industry 4.0 industrie i4.0",
    packages=find_packages(exclude=["tests", "continuous_integration"]),
    install_requires=[
        "aas-core-meta@git+https://github.com/aas-core-works/aas-core-meta@9ccd31e#egg=aas-core-meta",
        "aas-core-codegen@git+https://github.com/aas-core-works/aas-core-codegen@fcc252c#egg=aas-core-codegen",
        "aas-core3.0@git+https://github.com/aas-core-works/aas-core3.0-python@e232aa2#egg=aas-core3.0",
    ],
    py_modules=["test_codegen"],
)

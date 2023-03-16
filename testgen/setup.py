"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""
import os

from setuptools import setup, find_packages

# pylint: disable=redefined-builtin

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, "requirements.txt"), encoding="utf-8") as fid:
    install_requires = [line for line in fid.read().splitlines() if line.strip()]

setup(
    name="aas-core3.0-csharp-testgen",
    version="0.0.1",
    description="Generate the code of the unit tests on an AAS meta-model.",
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
    packages=find_packages(exclude=["tests", "continuous_integration", "dev_scripts"]),
    install_requires=install_requires,
    py_modules=["aas_core_3_0_rc2_csharp_testgen"],
    package_data={"aas_core_codegen": ["py.typed"]},
    data_files=[(".", ["requirements.txt"])],
)

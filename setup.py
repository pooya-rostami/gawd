from os import path
from setuptools import setup, find_packages
from codecs import open

with open(
    path.join(path.abspath(path.dirname(__file__)), "README.md"), encoding="utf-8"
) as f:
    long_description = f.read()

setup(
    name="gawd",
    version="1.0.0",
    license="LGPLv3",
    author="Pooya Rostami Mazrae, Alexandre Decan",
    url="https://github.com/pooya-rostami/gawd",
    description="GitHub Actions Workflow Differ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    keywords="github actions workflow diff change modification",
    packages=find_packages(include=["gawd"]),
    python_requires="~= 3.8",
    install_requires=[
        "ruamel.yaml ~= 0.17",
    ],
    extras_require={
        "test": ["pytest ~= 7.0"],
    },
    entry_points={
        "console_scripts": [
            "gawd=gawd:cli",
        ],
    },
    zip_safe=True,
)

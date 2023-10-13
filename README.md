# GAWD - GitHub Actions Workflow Differ

[![Tests](https://github.com/pooya-rostami/GAWD/actions/workflows/test.yaml/badge.svg?branch=master)](https://github.compooya-rostami/GAWD/actions/workflows/test.yaml)
[![License: LGPL v3](https://img.shields.io/badge/License-LGPL_v3-blue.svg)](https://www.gnu.org/licenses/lgpl-3.0)
[![PyPI](https://badgen.net/pypi/v/gawd)](https://pypi.org/project/gawd)
[![Commits](https://badgen.net/github/last-commit/pooya-rostami/GAWD)](https://github.com/pooya-rostami/GAWD/commits/)

The `GAWD` Python library and command-line tool provides a way to obtain all changes between two GitHub Actions workflow files. `GAWD` stands for **G**itHub **A**ctions **W**orkflow **D**iffer. 
Given two GitHub Actions workflow files, `GAWD` reports on the items that were added and removed, as well on items that were moved, renamed or changed based on their similarity. 

## Table of contents

  * [Installation](#installation)
  * [Documentation & usage](#documentation--usage)
  * [Contributions](#contributions)
  * [License](#license)


## Installation

`GAWD` comes as a command-line tool and as a reusable library for Python 3.8+. 

You can use `pip` to install it, as usual: `pip install GAWD`. This will install the latest available version from [PyPI](https://pypi.org/project/gawd).
Pre-releases are available from the *main* branch on [GitHub](https://github.com/pooya-rostami/GAWD)
and can be installed with `pip install git+https://github.com/pooya-rostami/GAWD`.


## Usage

### As a command-line tool

TODO

### As an importable library

TODO


## Contributions

Contributions are very welcome!
Feel free to report bugs or suggest new features using GitHub issues and/or pull requests.

## License

Distributed under [GNU Lesser General Public License v3](https://github.com/pooya-rostami/GAWD/blob/main/LICENSE.txt).

You can refer to this library using:

```
@software{gawd,
  author = {{Rostami Mazrae}, Pooya and Decan, Alexandre},
  title = {GAWD: GitHub Actions Workflow Differ},
  url = {https://github.com/pooya-rostami/GAWD},
}
```

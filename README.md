# gawd - GitHub Actions Workflow Differ

[![Tests](https://github.com/pooya-rostami/gawd/actions/workflows/test.yaml/badge.svg?branch=main)](https://github.com/pooya-rostami/gawd/actions/workflows/test.yaml)
[![License: LGPL v3](https://img.shields.io/badge/License-LGPL_v3-blue.svg)](https://www.gnu.org/licenses/lgpl-3.0)
[![PyPI](https://badgen.net/pypi/v/gawd)](https://pypi.org/project/gawd)
[![Commits](https://badgen.net/github/last-commit/pooya-rostami/gawd)](https://github.com/pooya-rostami/gawd/commits/)

The `gawd` Python library and command-line tool provides a way to obtain all changes between two GitHub Actions workflow files. `gawd` stands for **G**itHub **A**ctions **W**orkflow **D**iffer. 
Given two GitHub Actions workflow files, `gawd` reports on the items that were added and removed, as well on items that were moved, renamed or changed based on their similarity. 

## Table of contents

  * [Installation](#installation)
  * [Documentation & usage](#usage)
  * [Contributions](#contributions)
  * [License](#license)


## Installation

`gawd` comes as a command-line tool and as a reusable library for Python 3.8+. 

You can use `pip` to install it, as usual: `pip install gawd`. This will install the latest available version from [PyPI](https://pypi.org/project/gawd).
Pre-releases are available from the *main* branch on [GitHub](https://github.com/pooya-rostami/gawd)
and can be installed with `pip install git+https://github.com/pooya-rostami/gawd`.


## Usage

### As a command-line tool

The `gawd` command-line tool should be available in your shell. 
Otherwhise, you can call it using `python -m gawd`. 

```
usage: gawd [-h] [--threshold X] [--position-weight X] [--job-name-weight X] old new

gawd is a GitHub Actions Workflow Differ

positional arguments:
  old                   path to old workflow file
  new                   path to new workflow file

options:
  -h, --help            show this help message and exit
  --threshold X, -t X   distance threshold to map items, higher values favour "changed", "moved" and "renamed", lower values favour "added" and "removed"
                        (default is 0.5)
  --position-weight X, -p X
                        weight of item positions when comparing sequences (default is 0.1)
  --job-name-weight X, -j X   weight of job names when comparing jobs (default is 0.1)
```

**TODO**: Add an example


### As an importable library

`gawd` comes with two functions to compare workflow files, namely `diff_workflow_files` and `diff_workflows`. 
The former accepts the paths to two workflow files, load them and returns the output of `diff_workflows`. 
The latter accepts two workflows as Python dictionaries (e.g., loaded with `ruamel.yaml`) and returns a list of 4-uples `(kind, old_path, old_value, new_path, new_value)`.

The `kind` component is one of `added, removed, changed, moved, renamed` and indicates the kind of change. 
`old_path` and `new_path` correspond to a dotted notation indicating where the change occurred, while `old_value` and `new_value` correspond to the previous and new values, respectively. 
Notice that `old_path` and `old_value` are set to `None` in case of an "added" change. Similarly, `new_path` and `old_path` are `None` in case of a "removed" change. 

Similarly to the extra parameters that can be provided to the CLI tool, the `gawd` module exposes `THRESHOLD`, `POSITION_WEIGHT` and `JOB_NAME_WEIGHT`. 

**TODO**: Add an example


## Contributions

Contributions are very welcome!
Feel free to report bugs or suggest new features using GitHub issues and/or pull requests.

## License

Distributed under [GNU Lesser General Public License v3](https://github.com/pooya-rostami/gawd/blob/main/LICENSE.txt).

You can refer to this library using:

```
@software{gawd,
  author = {{Rostami Mazrae}, Pooya and Decan, Alexandre},
  title = {gawd: GitHub Actions Workflow Differ},
  url = {https://github.com/pooya-rostami/gawd},
}
```

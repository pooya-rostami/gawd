# gawd - GitHub Actions Workflow Differ

[![Tests](https://github.com/pooya-rostami/gawd/actions/workflows/test.yaml/badge.svg?branch=main)](https://github.com/pooya-rostami/gawd/actions/workflows/test.yaml)
[![License: LGPL v3](https://img.shields.io/badge/License-LGPL_v3-blue.svg)](https://www.gnu.org/licenses/lgpl-3.0)
[![PyPI](https://badgen.net/pypi/v/gawd)](https://pypi.org/project/gawd)
[![Commits](https://badgen.net/github/last-commit/pooya-rostami/gawd)](https://github.com/pooya-rostami/gawd/commits/)

`gawd` stands for **G**itHub **A**ctions **W**orkflow **D**iffer.
It is a Python library and command-line tool that computes all changes (i.e., diffs) between two GitHub Actions workflow files.
Given a pair of workflow files as input, and taking the specific syntax of GitHub Actions into account, `gawd` reports on the items that were added and removed, as well on items that were moved, renamed or changed based on their similarity.

## Table of contents

  * [Version](#version)
  * [Installation](#installation)
  * [Usage](#usage)
  * [Contributions](#contributions)
  * [License](#license)


## Installation

`gawd` can be used in two ways: as a command-line tool and as a reusable Python library.

You can use `pip install gawd` to install the latest available version from [PyPI](https://pypi.org/project/gawd).
Pre-releases are available from the *main* branch on [GitHub](https://github.com/pooya-rostami/gawd)
and can be installed with `pip install git+https://github.com/pooya-rostami/gawd`.

## Usage

### As a command-line tool

After installation, the `gawd` command-line tool should be available in your shell.
Otherwise, you can call it using `python -m gawd`.

```
usage: gawd [-h] [--threshold X] [--position-weight X] [--job-name-weight X] [--short] first second

gawd is a GitHub Actions Workflow Differ

positional arguments:
  first                 path to first workflow file
  second                path to second workflow file

options:
  -h, --help            show this help message and exit
  --threshold X, -t X   distance threshold to map items, higher values favours "changed", lower values favours
                        "added" and "removed" (default is 0.5)
  --position-weight X, -p X
                        weight of item positions when comparing sequences (default is 0.2)
  --job-name-weight X, -j X
                        weight of job names when comparing jobs (default is 0.2)
  --short, -s           limit the output of values to a few characters
```


The following example shows the output of the command line version of `gawd` when applied to compute the changes made to the workflow file main.yml which can be seen in [this commit](https://github.com/acidanthera/opencorepkg/commit/459849c8c3c16e74b22e4cdb346e73ce95e0a8db).
```python
>>> gawd old_main.yaml new_main.yaml --short
changed jobs.build-linux-clangpdb-gcc5.steps[1].run from "'sudo apt-get update (...) UB_PATH\n'" to "'sudo apt-get update (...) UB_PATH\n'"
renamed jobs.build-linux-clang38 to jobs.build-linux-clangdwarf
changed jobs.build-linux-clang38.name from "'Build Linux CLANG38'" to "'Build Linux CLANGDWARF'"
changed jobs.build-linux-clang38.env.TOOLCHAINS from "'CLANG38'" to "'CLANGDWARF'"
changed jobs.build-linux-clang38.steps[6].with.name from "'Linux CLANG38 Artifacts'" to "'Linux CLANGDWARF Artifacts'"
```

### As an importable library

`gawd` comes with two functions to compare workflow files, namely `diff_workflow_files` and `diff_workflows`.
The former accepts the paths to two workflow files, loads them and returns the output of `diff_workflows`.
The latter accepts two workflows as Python dictionaries (e.g., loaded with `ruamel.yaml`) and returns a list of 5-tuples `(kind, old_path, old_value, new_path, new_value)`.

The `kind` component is one of `added, removed, changed, moved, renamed` and indicates the kind of change.
`old_path` and `new_path` correspond to a dotted notation indicating where the change occurred, while `old_value` and `new_value` correspond to the previous and new values, respectively.
Notice that `old_path` and `old_value` are set to `None` in case of an "added" change. Similarly, `new_path` and `old_path` are `None` in case of a "removed" change.

Similarly to the extra parameters that can be provided to the CLI tool, the `gawd` module exposes `THRESHOLD`, `POSITION_WEIGHT` and `JOB_NAME_WEIGHT`.


The following example shows the output of the imported library version of `gawd` for the changes made to the workflow file `main.yml` in [this commit](https://github.com/acidanthera/opencorepkg/commit/459849c8c3c16e74b22e4cdb346e73ce95e0a8db).
```python
>>> from gawd import diff_workflow_files
>>> old_workflow_path = ...
>>> new_workflow_path = ...
>>> diff_workflow_files(old_workflow_path, new_workflow_path)
[('changed', 'jobs.build-linux-clangpdb-gcc5.steps[1].run', 'sudo apt-get update\nsudo apt-get install nasm ...', 'jobs.build-linux-clangpdb-gcc5.steps[1].run', 'sudo apt-get update\nsudo apt-get install nasm ...'),
('renamed', 'jobs.build-linux-clang38', {'name': 'Build Linux CLANG38', ...}, 'jobs.build-linux-clangdwarf', {'name': 'Build Linux CLANGDWARF', ...}),
('changed', 'jobs.build-linux-clang38.name', 'Build Linux CLANG38', 'jobs.build-linux-clangdwarf.name', 'Build Linux CLANGDWARF'),
('changed', 'jobs.build-linux-clang38.env.TOOLCHAINS', 'CLANG38', 'jobs.build-linux-clangdwarf.env.TOOLCHAINS', 'CLANGDWARF'),
('changed', 'jobs.build-linux-clang38.steps[6].with.name', 'Linux CLANG38 Artifacts', 'jobs.build-linux-clangdwarf.steps[6].with.name', 'Linux CLANGDWARF Artifacts')]
```

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

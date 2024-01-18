# gawd - GitHub Actions Workflow Differ

[![Tests](https://github.com/pooya-rostami/gawd/actions/workflows/test.yaml/badge.svg?branch=main)](https://github.com/pooya-rostami/gawd/actions/workflows/test.yaml)
[![License: LGPL v3](https://img.shields.io/badge/License-LGPL_v3-blue.svg)](https://www.gnu.org/licenses/lgpl-3.0)
[![PyPI](https://badgen.net/pypi/v/gawd)](https://pypi.org/project/gawd)
[![Commits](https://badgen.net/github/last-commit/pooya-rostami/gawd)](https://github.com/pooya-rostami/gawd/commits/)

`gawd` stands for **G**itHub **A**ctions **W**orkflow **D**iffer.
It is a Python library and command-line tool that computes all changes (i.e., diffs) between two GitHub Actions workflow files.
Given a pair of workflow files as input, and taking the specific syntax of GitHub Actions into account, `gawd` reports on the items that were added and removed, as well on items that were moved, renamed or changed based on their similarity.


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
usage: gawd [-h] [--threshold X] [--position-weight X] [--job-name-weight X]
            [--short] [--json] [--verbose]
            first second

gawd is an open source GitHub Actions Workflow Differencing tool that is aware
of the specific workflow syntax of GitHub Actions workflows. Given a pair of
workflow files as input, the tool reports on the items that were added and
removed, as well on items that were moved, renamed or changed based on their
similarity.

positional arguments:
  first                 path to first workflow (YAML) file
  second                path to second workflow (YAML) file

optional arguments:
  -h, --help            show this help message and exit
  --threshold X, -t X   ranged from 0 to 1, distance threshold to map items,
                        value closer to 1 favours "changed", value closer to 0
                        favours "added" and "removed" (default is 0.5)
  --position-weight X, -p X
                        ranged from 0 to 1, weight of item positions when
                        comparing sequences (default is 0.2)
  --job-name-weight X, -j X
                        ranged from 0 to 1, weight of job names when comparing
                        jobs (default is 0.2)
  --short, -s           limit the output of values to a few characters
  --json                output in json
  --verbose             output in more detail
```


#### Examples:
Let us take the changes made to the workflow file "main.yml" in [this commit](https://github.com/acidanthera/opencorepkg/commit/459849c8c3c16e74b22e4cdb346e73ce95e0a8db) as an example.

`--short` Condensed output of `gawd` when applied to compute the changes:
```python
>>> gawd old_main.yaml new_main.yaml --short
changed jobs.build-linux-clangpdb-gcc5.steps[1].run from "'sudo apt-get update (...) UB_PATH\n'" to "'sudo apt-get update (...) UB_PATH\n'"
renamed jobs.build-linux-clang38 to jobs.build-linux-clangdwarf
changed jobs.build-linux-clang38.name from "'Build Linux CLANG38'" to "'Build Linux CLANGDWARF'"
changed jobs.build-linux-clang38.env.TOOLCHAINS from "'CLANG38'" to "'CLANGDWARF'"
changed jobs.build-linux-clang38.steps[6].with.name from "'Linux CLANG38 Artifacts'" to "'Linux CLANGDWARF Artifacts'"
```

`--json` To output the results in JSON format:
```python
>>> gawd old_main.yaml new_main.yaml --short --json
[{"type": "changed", "old": {"path": "jobs.build-linux-clangpdb-gcc5.steps[1].run", "value": "'sudo apt-get update (...) UB_PATH\\n'"}, "new": {"path": "jobs.build-linux-clangpdb-gcc5.steps[1].run", "value": "'sudo apt-get update (...) UB_PATH\\n'"}},
{"type": "renamed", "old": {"path": "jobs.build-linux-clang38", "value": "{'name': 'Build Linu (...) *.zip'}}]}"}, "new": {"path": "jobs.build-linux-clangdwarf", "value": "{'name': 'Build Linu (...) *.zip'}}]}"}},
{"type": "changed", "old": {"path": "jobs.build-linux-clang38.name", "value": "'Build Linux CLANG38'"}, "new": {"path": "jobs.build-linux-clangdwarf.name", "value": "'Build Linux CLANGDWARF'"}},
{"type": "changed", "old": {"path": "jobs.build-linux-clang38.env.TOOLCHAINS", "value": "'CLANG38'"}, "new": {"path": "jobs.build-linux-clangdwarf.env.TOOLCHAINS", "value": "'CLANGDWARF'"}},
{"type": "changed", "old": {"path": "jobs.build-linux-clang38.steps[6].with.name", "value": "'Linux CLANG38 Artifacts'"}, "new": {"path": "jobs.build-linux-clangdwarf.steps[6].with.name", "value": "'Linux CLANGDWARF Artifacts'"}}]
```

`--threshold` A value between 0 and 1 representing the sensitivity of `gawd` in identifying changes. A higher threshold results in more instances of 'changed' or 'renamed', while a lower threshold favours 'added' or 'removed':

```python
>>> gawd old_main.yaml new_main.yaml --short --threshold 0.1
removed jobs.build-linux-clangpdb-gcc5.steps[1] with {'name': 'Install De (...) B_PATH\n'}
added jobs.build-linux-clangpdb-gcc5.steps[1] with {'name': 'Install De (...) B_PATH\n'}
removed jobs.build-linux-clang38 with {'name': 'Build Linu (...) *.zip'}}]}
added jobs.build-linux-clangdwarf with {'name': 'Build Linu (...) *.zip'}}]}
```

### As an importable library

`gawd` comes with two functions to compare workflow files, namely `diff_workflow_files` and `diff_workflows`.
The former accepts the paths to two workflow files, loads them and returns the output of `diff_workflows`.
The latter accepts two workflows as Python dictionaries (e.g., loaded with `ruamel.yaml`) and returns a list of 5-tuples `(kind, old_path, old_value, new_path, new_value)`.

The `kind` component is one of `added, removed, changed, moved, renamed` and indicates the kind of change.
`old_path` and `new_path` correspond to a dotted notation indicating where the change occurred, while `old_value` and `new_value` correspond to the previous and new values, respectively.
Notice that `old_path` and `old_value` are set to `None` in case of an "added" change, and `new_path` and `old_path` are `None` in case of a "removed" change.

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

This tool is distributed under [GNU Lesser General Public License v3](https://github.com/pooya-rostami/gawd/blob/main/LICENSE.txt).


## Citing

You can refer to the scientific publication describing this tool using
```
@inproceedings{gawd2024MSR,
  author = {{Rostami Mazrae}, Pooya and Decan, Alexandre and Mens, Tom},
  title = {gawd: A Differencing Tool for GitHub Actions Workflows},
  booktitle = {International Conference on Mining Software Repositories - Data and Tools Showcase Track},
  year = 2024
}
```

You can also refer to this tool directly using:

```
@software{gawd2023,
  author = {{Rostami Mazrae}, Pooya and Decan, Alexandre},
  title = {gawd: GitHub Actions Workflow Differ},
  url = {https://github.com/pooya-rostami/gawd},
  year = 2023,
  institute = {Software Engineering Lab at University of Mons, Belgium}
}
```

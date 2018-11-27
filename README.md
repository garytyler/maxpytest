
[![PyPI version](https://badge.fury.io/py/maxpytest.svg)](https://badge.fury.io/py/maxpytest)
[![Build status](https://ci.appveyor.com/api/projects/status/eonytxoyfg9cs33v?svg=true)](https://ci.appveyor.com/project/garytyler/maxpytest-dbke3)
[![codecov](https://codecov.io/gh/garytyler/maxpytest/branch/master/graph/badge.svg?token=JseFmmlQHm)](https://codecov.io/gh/garytyler/maxpytest)

# Overview

Command line tool for a friendly testing workflow using the [Pytest](https://docs.pytest.org/en/latest/)  framework in 3ds Max

* Run tests with all 3ds Max Python APIs, including GUI/PySide2 libraries
* Source dependencies from a [pipenv](https://pipenv.readthedocs.io/en/latest/) virtual environment
* Automate a new 3ds Max/python session for each tests invocation

## Setup

### Install with pip

Install with pip using Python 2.7:

```ps
pip install maxpytest
```

## Usage

Due to the caching mechanism of python's import system and Pytest's design, changes made to test files (and any modules they import) will not be reflected in subsequent Pytest invocations _in the same python process_. This means ensuring that your changes are reflected requires a restart of the 3ds Max/python session.

The argument `-m/--max` directs `maxpytest` how to run your tests. For maxpytest to handle closing and relaunching 3ds Max automatically, [run your tests using MXSPyCOM](#Run-your-tests-using-MXSPyCOM). For a simple setup, or if targeting multiple 3ds Max versions, [run your tests directly with 3ds Max](#Run-your-tests-directly-with-3ds-Max). To use the first discovered method, [run your tests using the default run method](#Run-your-tests-using-the-default-run-method).

### Including site-packages from a pipenv virtual environment

If the current working directory is a project root with an installed [pipenv](https://pipenv.readthedocs.io/en/latest/) virtual environment, that environment's site-packages are made available to the 3ds Max python environment running the tests. Overriding the current working directory with `--cwd` effects this behavior accordingly.

If no [pipenv](https://pipenv.readthedocs.io/en/latest/) virtual environment is discovered in the current working directory and the virtual environment includes a pytest package, that pytest package is used to run the tests. Otherwise maxpytest's pytest dependency is used.

To install pipenv, run from your project root:

```ps
pip install pipenv
```

Then, setup a pipenv virtual environment:

```ps
pipenv --python 2.7 install
```

Add pytest to the virtual environment:

```ps
pipenv install pytest
```

### Run your tests using MXSPyCOM

When you run your tests with [MXSPyCOM](https://github.com/JeffHanna/MXSPyCOM), the closing and relaunching 3ds Max is handled automatically. Any unsaved work will trigger a prompt to save it before closing. For more about [MXSPyCOM](https://github.com/JeffHanna/MXSPyCOM) see the [wiki](https://github.com/JeffHanna/MXSPyCOM/wiki).

To invoke your tests, use `maxpytest -m [path to MXSPyCOM.exe] -py [pytest args]`, with Pytest args following `-py` or `--pytest` as the final command argument.

For example:

```ps
# Relaunch 3ds Max then invoke pytest from current working dir with verbose
maxpytest -m "C:\\Program Files\\MXSPyCOM\\MXSPyCOM.exe" -py -v .

# Relaunch 3ds Max then invoke pytest in directory ./tests
maxpytest -m "C:\\Program Files\\MXSPyCOM\\MXSPyCOM.exe" -py tests/

# Skip relaunch and just invoke pytest in directory ./tests
maxpytest -m "C:\\Program Files\\MXSPyCOM\\MXSPyCOM.exe" --no-restart -py tests/
```

Test results print to the 3ds Max Listener.

### Run your tests directly with 3ds Max

To run tests in 3ds max without using MXSPyCOM, use `-m/--max` with the version year of the 3ds Max you wish to target, or a full path to 3dsmax.exe.

For example:

```ps
# Invoke pytest from current working dir in a new instance of 3ds Max 2019
maxpytest -m "C:\\Program Files\\Autodesk\\3ds Max 2019\\3dsmax.exe"

# Invoke pytest from current working dir in a new instance of 3ds Max 2019
maxpytest -m 2019

# Invoke pytest from current working dir and run tests in ./tests
maxpytest -m 2016 -py tests/ -v
```

Test results will print to the 3ds Max Listener.

### Run your tests using the default run method

If `maxtest` is used without a `-m/--max` argument, maxpytest will search for MXSPyCOM.exe at `C:\Program Files\MXSPyCOM\MXSPyCOM.exe`. If not found, the most recent version of 3ds Max installed on the system will be used.

## Contact

For questions, support, or feature requests, please open an issue or reach out at mail@garytyler.com .

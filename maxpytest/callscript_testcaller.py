from __future__ import print_function
import os
import sys
import imp
import site
import subprocess as sp


class HandlePytestQt(object):
    def __init__(self, args):
        self.args = args

    def pytest_load_initial_conftests(self, early_config, parser, args):
        early_config.pluginmanager.set_blocked("pytest-qt")


def _get_venv_path(cwd):
    """Returns pipenv virtual environment's site-packages path."""
    proc = sp.Popen(r"pipenv --venv", cwd=cwd, stdout=sp.PIPE, shell=True)
    venvpath = proc.communicate()[0].rstrip()
    if not os.path.exists(venvpath):
        raise RuntimeError
    return venvpath


def add_project_sitepkgs(cwd):
    """Get site-packages directory from given project path's virtual environment to
    current python environment and print report.

    :param cwd: root directory path for an installed Python virtual environment
    :type cwd: str
    """
    try:
        venvpath = _get_venv_path(cwd)
    except RuntimeError:
        sitepkgs = "None"
    else:
        sitepkgs = os.path.join(venvpath, r"Lib", r"site-packages")
        sys.path.insert(0, sitepkgs)
        site.addsitedir(sitepkgs)
    finally:
        print("additional site-pkgs:", sitepkgs)


def patch_isatty():
    """Add a mocked method to handle pytest expectations in 3ds Max. More:
    https://cbuelter.wordpress.com/2014/10/21/running-pytest-inside-3ds-max/
    """

    def _isatty(*args, **kwargs):
        return False

    sys.stdout.isatty = _isatty


def import_pytest(default_pytest_src):
    """If attempted pytest import fails, import using given module_path.

    :param default_pytest_src: file path of a 'pytest.pyc' in another python
        environment's site-packages
    :type default_pytest_src: path string
    :return: available pytest module
    :rtype: module
    """
    try:
        import pytest
    except ImportError:
        default_src_sitepkgs = os.path.abspath(os.path.dirname(default_pytest_src))
        site.addsitedir(default_src_sitepkgs)
        import pytest

        sys.path.remove(default_src_sitepkgs)
    finally:
        return pytest


def prep_environment(cwd):
    patch_isatty()
    os.chdir(cwd)


def get_args(pytestargs):
    """Add arg to turn off capturing of filedescriptors
    """
    # TODO Replace with plugin hook
    return pytestargs + [r"--capture=sys"]


def call_tests(cwd, pytestargs, default_pytest_src):
    """Main function to be called from callblock
    """
    add_project_sitepkgs(cwd)
    pytest = import_pytest(default_pytest_src)
    prep_environment(cwd)
    args = pytestargs + [r"--capture=sys"]
    try:
        pytest.main(args=args, plugins=[HandlePytestQt(args)])
    except Exception as e:
        print(e, "Pytest args:", args)
        raise e

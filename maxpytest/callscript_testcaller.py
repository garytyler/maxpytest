from __future__ import print_function
import os
import sys
import imp
import site
import shutil
import tempfile
import subprocess as sp


class HandlePytestQt(object):
    def __init__(self, args):
        self.args = args

    def pytest_load_initial_conftests(self, early_config, parser, args):
        early_config.pluginmanager.set_blocked("pytest-qt")


def _get_proj_venv_path(cwd):
    """Returns pipenv virtual environment's site-packages path."""
    proc = sp.Popen(r"pipenv --venv", cwd=cwd, stdout=sp.PIPE)
    venvpath = proc.communicate()[0].rstrip()
    if not os.path.exists(venvpath):
        raise RuntimeError
    return venvpath


def _create_venv_with_pytest(rootdir):
    """Creates a pipenv virtual environment at root rootdir, and install pytest in the
    virtual environment installed.
    """
    if os.path.exists(rootdir):
        shutil.rmtree(rootdir)
    os.mkdir(rootdir)
    p1 = sp.Popen(r"pipenv install pytest", cwd=rootdir)
    p1.wait()
    if not (p1.returncode is 0):
        raise RuntimeError


def _get_temp_venv_path():
    """Look for a temporary pipenv virtual environment with pytest installed at
    temproot and returns it's path. If one is not found, create one and return it's
    path.
    """
    temproot = os.path.join(tempfile.gettempdir(), "maxpytest_temp_venv")
    if os.path.exists(temproot):
        try:
            venvpath = _get_proj_venv_path(temproot)
        except RuntimeError:
            pass
        else:
            return venvpath
    _create_venv_with_pytest(temproot)
    return _get_proj_venv_path(temproot)


def add_sitepkgs(cwd):
    """Get site-packages directory from given project path's virtual environment to
    current python environment and print report.

    :param cwd: root directory path for an installed Python virtual environment
    :type cwd: str
    """
    try:
        venvpath = _get_proj_venv_path(cwd)
    except RuntimeError:
        venvpath = _get_temp_venv_path()
    finally:
        sitepkgs = os.path.join(venvpath, r"Lib", r"site-packages")
        sys.path.insert(0, sitepkgs)
        site.addsitedir(sitepkgs)
        print("additional site-pkgs:", sitepkgs)
        return True


def patch_isatty():
    """Add a mocked method to handle pytest expectations in 3ds Max. More:
    https://cbuelter.wordpress.com/2014/10/21/running-pytest-inside-3ds-max/
    """

    def _isatty(*args, **kwargs):
        return False

    sys.stdout.isatty = _isatty


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
    add_sitepkgs(cwd)
    import pytest

    prep_environment(cwd)

    args = pytestargs + [r"--capture=sys"]
    try:
        pytest.main(args=args, plugins=[HandlePytestQt(args)])
    except Exception as e:
        print(e, "Pytest args:", args)
        raise e

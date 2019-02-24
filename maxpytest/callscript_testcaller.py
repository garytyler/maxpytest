from __future__ import print_function
import os
import re
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


def _get_proj_venv_path(cwd, pyexe):
    """Returns pipenv virtual environment's site-packages path."""
    proc = sp.Popen(r"{0} -m pipenv --venv".format(pyexe), cwd=cwd, stdout=sp.PIPE)
    venvpath = proc.communicate()[0].rstrip()
    if not os.path.exists(venvpath):
        raise RuntimeError
    return venvpath


def _create_venv_with_pytest(rootdir, pyexe):
    """Creates a pipenv virtual environment at root rootdir, and install pytest in the
    virtual environment installed.
    """
    if os.path.exists(rootdir):
        shutil.rmtree(rootdir)
    os.mkdir(rootdir)
    p1 = sp.Popen(r"{0} -m pipenv install pytest".format(pyexe), cwd=rootdir)
    p1.wait()
    if 0 != p1.returncode:
        raise RuntimeError


def _get_temp_venv_path(pyexe):
    """Look for a temporary pipenv virtual environment with pytest installed at
    temproot and returns it's path. If one is not found, create one and return it's
    path.
    """
    temproot = os.path.join(tempfile.gettempdir(), "maxpytest_temp_venv")
    if os.path.exists(temproot):
        try:
            venvpath = _get_proj_venv_path(temproot, pyexe)
        except RuntimeError:
            pass
        else:
            return venvpath
    _create_venv_with_pytest(temproot, pyexe)
    return _get_proj_venv_path(temproot, pyexe)


def add_sitepkgs(cwd, pyexe):
    """Get site-packages directory from given project path's virtual environment to
    current python environment and print report.

    :param cwd: root directory path for an installed Python virtual environment
    :type cwd: str
    """
    try:
        venvpath = _get_proj_venv_path(cwd, pyexe)
    except RuntimeError:
        venvpath = _get_temp_venv_path(pyexe)
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


def expand_combo_args(arglist):
    """For each combo arg in a list of command ling arg strings, replace it with multiple single args. A combo arg is is multiple single character flags combined into one, such as ['-abc'] which is interpreted as ['-a', '-b', '-c'].

    Arguments:
        arg {list} -- List of command line argument strings

    Returns:
        list -- Return a list in which all combo args have been expanded into multiple args.
    """
    pattern = re.compile(r"(?<=^-)[a-z]{2,}$")

    result = []
    for a in arglist:
        combo_arg = re.search(pattern, a)
        if combo_arg:
            for i in list(combo_arg.group(0)):
                result.append("-" + i)
        else:
            result.append(a)

    return result


def handle_pytest_args(pytestargs):
    """Add arg to turn off capturing of filedescriptors
    """
    resultargs = expand_combo_args(pytestargs)

    badargs = [a for a in resultargs if a in ["--capture=fd"]]
    for arg in badargs:
        resultargs.remove(arg)

    nocapargs = [a for a in resultargs if a in ["--capture=sys", "--capture=no", "-s"]]
    if not any(nocapargs):
        resultargs.append("--capture=sys")

    return resultargs


def call_tests(cwd, pytestargs, pyexe):
    """Main function to be called from callblock
    """
    add_sitepkgs(cwd, pyexe)
    import pytest

    prep_environment(cwd)

    args = handle_pytest_args(pytestargs)
    try:
        pytest.main(args=args, plugins=[HandlePytestQt(args)])
    except Exception as e:
        print(e, "Pytest args:", args)
        raise e

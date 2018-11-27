from __future__ import print_function
import os
import sys
import pytest
import inspect
import importlib
from maxpytest import callscripts
from maxpytest import callscript_testcaller


def test_create_testcaller_cwd_is_accurate(mixedstr, mixedlist):
    script_path = callscripts.create_testcaller(cwd=mixedstr, pytestargs=mixedlist)
    with open(script_path) as f:
        result_lines = f.readlines()
    # String cwd is included in 1 line
    assert 1 is len([str(l) for l in result_lines if mixedstr in l])


def test_create_testcaller_pytestargs_is_accurate(mixedstr, mixedlist):
    script_path = callscripts.create_testcaller(cwd=mixedstr, pytestargs=mixedlist)
    with open(script_path) as f:
        result_lines = f.readlines()
    # String pytestargs is included in 1 line
    assert 1 is len(
        [
            line
            for line in result_lines
            if str([str(arg).replace("\\", r"\\") for arg in mixedlist]) in line
        ]
    )


def test_create_restarter(mixedstr):
    scriptpath = callscripts.create_restarter(launchscript=mixedstr)
    with open(scriptpath) as f:
        result_lines = f.readlines()
    # String launchscript is included in 1 line
    assert 1 is len([str(l) for l in result_lines if mixedstr in l])


def test_import_caller_script(mixedstr, mixedlist):
    """New test caller script imports as module including TestCaller class."""
    scriptpath = callscripts.create_testcaller(cwd=mixedstr, pytestargs=mixedlist)
    script_parent_dir = os.path.dirname(scriptpath)
    sys.path.insert(1, script_parent_dir)
    basename = os.path.basename(scriptpath)
    modname = os.path.splitext(basename)[0]
    module = importlib.import_module(modname)
    # created callscriptscript imports successfully
    assert module
    created_script = inspect.getsource(module)
    template_script = inspect.getsource(callscript_testcaller)
    # text in template_script is in created_script
    assert template_script in created_script

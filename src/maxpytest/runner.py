#!/usr/bin/env python2
from __future__ import print_function
import os
import sys
import inspect
import tempfile
import subprocess
import maxcom
import callscripts


def is_year(arg):
    stringarg = str(arg)
    yearlength = 2 <= len(stringarg) <= 4
    isnum = stringarg.isdigit()
    return yearlength and isnum

def _get_scriptrunner(runnerarg):
    is_string = isinstance(runnerarg, str)
    if runnerarg is None:
        return _get_default_scriptrunner()
    elif is_year(runnerarg):
        return maxcom.UserMax(versionyear=runnerarg)
    elif is_string and os.path.basename(runnerarg) == maxcom.UserMax.filename:
        return maxcom.UserMax(exepath=runnerarg)
    elif is_string and os.path.basename(runnerarg) == maxcom.MXSPyCOM.filename:
        return maxcom.MXSPyCOM(exepath=runnerarg)
    raise ValueError(runnerarg)

def _get_default_scriptrunner():
    scriptrunner = None
    for ScriptRunner in [maxcom.MXSPyCOM, maxcom.UserMax]:
        try:
            scriptrunner = ScriptRunner()
        except RuntimeError as e:
            continue
        else:
            break
    if not scriptrunner:
        raise e
    else:
        return scriptrunner

def _get_existing_working_dir(cwd):
    if not cwd:
        return os.getcwd()
    elif os.path.exists(cwd):
        return cwd
    else:
        raise ValueError(cwd)

def runtests(cwd, runnerarg, pytestargs, restart):
    existing_cwd = _get_existing_working_dir(cwd)
    testcaller = callscripts.create_testcaller(cwd=existing_cwd,
                                               pytestargs=pytestargs)
    scriptrunner = _get_scriptrunner(runnerarg=runnerarg)
    
    if restart and scriptrunner.filename == maxcom.MXSPyCOM.filename:
        restarter = callscripts.create_restarter(launchscript=testcaller)
        scriptrunner.run_script(scriptpath=restarter)
    else:
        scriptrunner.run_script(scriptpath=testcaller)

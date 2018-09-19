#!/usr/bin/env python2
from __future__ import print_function
import os
import inspect
import tempfile
import callscript_testcaller
import callscript_restarter


def _create_caller(filename, callblock, sourcemodule=None):
    path = os.path.join(tempfile.gettempdir(), filename)
    if sourcemodule:
        body = inspect.getsource(sourcemodule)
        lines = (body, '\n', callblock, '\n')
    else:
        lines = (callblock, '\n')
    with open(path, 'w') as f:
        for line in lines:
            f.write(line)
    return path

def create_testcaller(cwd, pytestargs):    
    _pytestargs = [] if pytestargs is None else pytestargs
    _sourcemodule = callscript_testcaller
    _filename = 'maxpytest_testcaller.py'
    _callblock = r"""if __name__ == '__main__':
    try:
        call_tests('{0}', {1})
    except Exception as e:
        print(e)
    """.format(cwd, _pytestargs) 
    return _create_caller(filename=_filename, 
                          callblock=_callblock,
                          sourcemodule=_sourcemodule)

def create_restarter(launchscript=None):
    _sourcemodule = callscript_restarter
    _filename = 'maxpytest_restarter.py'
    _callblock = r"""if __name__ == '__main__':
    restart('{0}')
    """.format(launchscript) 
    return _create_caller(filename=_filename,
                          callblock=_callblock,
                          sourcemodule=_sourcemodule)

#!/usr/bin/env python2
from __future__ import print_function
import os
import pytest
import subprocess as sp
from maxpytest import callscripts
 
@pytest.fixture(scope='module')
def tempcwd(tmpdir_factory):
    return str(tmpdir_factory.mktemp('cwd'))

@pytest.fixture(scope='class')
def mock_venv(tempcwd):
    """Create a mock virtual environment to use as source project for testing testcaller script 
    """
    def run_command(command, cwd):
        return sp.Popen(command, cwd=cwd, stdout=sp.PIPE, stderr=sp.STDOUT)

    def _setup():
        try:
            _process = run_command(r'pipenv --python 2.7 install', tempcwd)
        except:
            _teardown()
            raise
        else:
            _process.wait()
            return _process

    def _teardown():
        try:
            _process = run_command(r'pipenv --rm', tempcwd)
        except:
            pass
        else:
            _process.wait()
            return _process

    if _setup().returncode is 0:
        yield tempcwd
    else:
        pytest.fail(setup_process.output)

    _teardown()

@pytest.fixture
def testcaller(mocker, monkeypatch, request):
    """Patch testcaller attributes required for call_tests to run()"""
    import maxpytest.callscript_testcaller as _testcaller
    mocker.patch.object(_testcaller, 'patch_isatty')
    mocker.patch.object(_testcaller.os, 'chdir')
    yield _testcaller

class TestExpectedCalls(object):
    def test_patch_isatty(self, testcaller, mock_venv):
        testcaller.prep_environment(cwd=mock_venv)
        testcaller.patch_isatty.assert_called_once_with()

    def test_os_chdir(self, testcaller, mock_venv):
        testcaller.prep_environment(cwd=mock_venv)
        testcaller.os.chdir.assert_called_once_with(mock_venv)

    def test_get_pytest(self, mocker, testcaller, mock_venv):
        assert testcaller.get_pytest(cwd=mock_venv)

    def test_pytest_main(self, mocker, testcaller, mock_venv):
        mocker.patch.object(testcaller.pytest, 'main', autospec=True)

        _pytestargs = []
        _args = testcaller.get_args(_pytestargs)

        testcaller.call_tests(cwd=mock_venv, pytestargs=_pytestargs)
        testcaller.pytest.main.assert_called_once_with(_args)

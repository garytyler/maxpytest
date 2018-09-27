#!/usr/bin/env python2
from __future__ import print_function
import os
import pytest
import subprocess as sp
from maxpytest import callscripts

# TODO def imported_pytest_is_from_maxpytest_sitepkgs_if_not_avail_in_added
# TODO def imported_pytest_is_from_added_sitepkgs_if_avail_in_added

@pytest.fixture(scope='module')
def tempcwd(tmpdir_factory):
    return str(tmpdir_factory.mktemp('cwd'))

@pytest.fixture(scope='class')
def mock_cwd(tempcwd):
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
    
    setup_process = _setup()
    if setup_process.returncode is 0:
        yield tempcwd
    else:
        pytest.fail(setup_process)

    _teardown()

@pytest.fixture
def testcaller(mocker, monkeypatch, request):
    """Patch testcaller attributes required for call_tests to run()"""
    import maxpytest.callscript_testcaller as _testcaller
    mocker.patch.object(_testcaller, 'patch_isatty')
    mocker.patch.object(_testcaller.os, 'chdir')
    yield _testcaller

class TestExpectedCalls(object):
    def test_patch_isatty(self, testcaller, mock_cwd):
        testcaller.prep_environment(cwd=mock_cwd)
        testcaller.patch_isatty.assert_called_once_with()

    def test_os_chdir(self, testcaller, mock_cwd):
        testcaller.prep_environment(cwd=mock_cwd)
        testcaller.os.chdir.assert_called_once_with(mock_cwd)

    def test_import_pytest(self, mocker, testcaller, mock_cwd):
        assert testcaller.import_pytest(mxpt_sitepkgs=mock_cwd)

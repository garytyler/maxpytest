#!/usr/bin/env python2
from __future__ import print_function
import os
import pytest
from maxpytest import runner
from maxpytest import callscripts


@pytest.fixture
def mock_UserMax(mocker):
    _filename = getattr(runner.maxcom, 'UserMax').filename
    return mocker.patch.object(runner.maxcom, 'UserMax', autospec=True)

@pytest.fixture
def mock_MXSPyCOM(mocker):
    _filename = getattr(runner.maxcom, 'MXSPyCOM').filename
    return mocker.patch.object(runner.maxcom, 'MXSPyCOM', autospec=True)

def test_runtests_default_calls_UserMax(tmpdir, mocker, mock_UserMax):
    def raise_runtime_error(x):
        raise RuntimeError
    mocker.patch.object(runner.maxcom.MXSPyCOM,
                        '_get_default_exepaths',
                        raise_runtime_error)
    runner.runtests(cwd=str(tmpdir),
                     runnerarg=None,
                     pytestargs=[], 
                     restart=None)
    mock_UserMax.assert_called_once_with()

def test_runtests_with_restart_creates_restarter(mocker, tmpdir, tmpfile):
    cwdpath = str(tmpdir)
    tmpexefile = str(tmpfile('root', runner.maxcom.MXSPyCOM.filename))
    testcaller = callscripts.create_testcaller(cwd=cwdpath, pytestargs=[])
    
    mocker.patch.object(runner.maxcom.MXSPyCOM, 'run_script')
    create_restarter = mocker.patch.object(runner.callscripts,
                                           'create_restarter')
    
    runner.runtests(cwd=cwdpath,
                    runnerarg=tmpexefile,
                    pytestargs=[],
                    restart=True)
    
    create_restarter.assert_called_once_with(launchscript=testcaller)

def test_runtests_default_no_max_installed_raises(mocker, tmpdir,
                                                  patch_max_root_env_vars):
    tmpdirpath = str(tmpdir)
    patch_max_root_env_vars([])
    mocker.patch.object(runner.maxcom.MXSPyCOM,
                        '_get_default_exepaths',
                        lambda x: '')
    with pytest.raises(RuntimeError) as e:
        runner.runtests(cwd=tmpdirpath,
                         runnerarg=None,
                         pytestargs=['-r'], 
                         restart=None)

@pytest.mark.parametrize('runnerarg, exception',
                         [(2019, None), (2014, None), (14, None),
                          (4, ValueError), (20199, ValueError)])
def test_runtests_with_year(mocker, tmpdir, runnerarg, exception):
    def do_runtests():
        runner.runtests(cwd=None,
                        runnerarg=runnerarg,
                        pytestargs=[],
                        restart=None)
    mocker.patch.object(runner.maxcom, 'UserMax')
    mocker.patch.object(runner.maxcom, 'MXSPyCOM')
    if exception is None:
        do_runtests()
        runner.maxcom.UserMax.assert_called_once()
    elif exception:
        with pytest.raises(exception):
            do_runtests()
    runner.maxcom.MXSPyCOM.assert_not_called()

@pytest.mark.parametrize('called, not_called',
                        [('MXSPyCOM', 'UserMax'),
                         ('UserMax', 'MXSPyCOM')])
def test_runtests_with_exepath(mocker, tmpdir, called, not_called):

    called_filename = getattr(runner.maxcom, called).filename
    mock_called = mocker.patch.object(runner.maxcom, called,
                                       filename=called_filename)
    not_called_filename = getattr(runner.maxcom, not_called).filename
    mock_not_called = mocker.patch.object(runner.maxcom, not_called,
                                           filename=not_called_filename)
    runner.runtests(cwd=str(tmpdir),
                    runnerarg=os.path.join('C:', 'path', called_filename),
                    pytestargs=[],
                    restart=None)
    mock_called.assert_called_once()
    mock_not_called.assert_not_called()



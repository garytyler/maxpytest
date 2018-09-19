#!/usr/bin/env python2
from __future__ import print_function
import os
import sys
import pytest
from maxpytest import cli

@pytest.mark.parametrize('cliargs, cwd, runnerarg, pytestargs, restart',
                        [([],
                          None, None, None, True),
                    
                         (['--max', '2019'],
                          None, '2019', None, True),

                         (['-m', 'C:\\path\\dir\\MXSPyCOM'],
                          None, 'C:\\path\\dir\\MXSPyCOM', None, True),

                         (['--cwd', 'C:\\path\\dir\\'],
                          'C:\\path\\dir\\', None, None, True),

                         (['--no-restart'],
                          None, None, None, False),
                        
                         (['--py', '-x', '-s', '-v', '/path/dir'],
                          None, None, ['-x', '-s', '-v', '/path/dir'], True),
                          
                          ])
def test_parse(cliargs, cwd, runnerarg, pytestargs, restart,
               tmpdir, mocker, monkeypatch):
    """Test that given cliargs result in expected arguments being passed to runner.runtests()
    
    :type cliargs: list
    :type cwd: str
    :type runnerarg: str
    :type pytestargs: list
    :type restart: bool
    """
    tempcwd = str(tmpdir.mkdir('cwd'))
    monkeypatch.setattr(cli.sys, 'argv', [tempcwd] + cliargs)
    cli_runtests = mocker.patch.object(cli.runner, 'runtests', autospec=True)
    cli.main()
    cli_runtests.assert_called_once_with(cwd=cwd,
                                         runnerarg=runnerarg,
                                         pytestargs=pytestargs,
                                         restart=restart)

#!/usr/bin/env python2
from __future__ import print_function
import os
import pytest
from maxpytest.maxcom import CommandExecutor
from maxpytest.maxcom import MXSPyCOM
from maxpytest.maxcom import UserMax

# TODO def test_MXSPyCOM_run_script_succeeds():
# TODO def test_UserMax_run_script_succeeds():
# TODO def test_UserMax_init_with_defaults_fails():
# TODO def test_UserMax_init_with_defaults_succeeds():
# TODO def test_UserMax_init_with_year_and_path_fails():

@pytest.mark.parametrize('klass', [MXSPyCOM, UserMax])
def test_init_w_valid_path_succeeds(klass, tmpfile):
    exepath = str(tmpfile(dirname='exe_root_dir',
                          filename=klass.filename))
    com = klass(exepath=exepath)
    assert os.path.isfile(com.exe)
    assert os.path.isdir(com.root)

@pytest.mark.parametrize('klass', [MXSPyCOM, UserMax])
def test_init_w_invalid_exepath_fails(klass, tmpfile):
    exepath = str(tmpfile(dirname='root_dir', 
                          filename=klass.filename))
    com = klass(exepath=exepath)
    assert os.path.isfile(com.exe)
    assert os.path.basename(com.exe) == klass.filename
    with pytest.raises(ValueError):
        exepath = str(tmpfile(dirname='bad_filename_dir',
                              filename='bad_filename_file'))
        klass(exepath=exepath)
    with pytest.raises(ValueError):
        klass(exepath='path_does_not_exist')

@pytest.mark.parametrize('year_to_patch', UserMax.supported_version_years)
def test_UserMax_init_find_default_UserMax_succeeds(patch_max_root_env_vars,
                                                    year_to_patch,
                                                    tmpdir,
                                                    tmpfile):
    patch_max_root_env_vars([year_to_patch])
    com = UserMax(versionyear=None, exepath=None)
    assert os.path.isfile(com.exe)
    assert os.path.basename(com.exe) == UserMax.filename
    with pytest.raises(ValueError):
        UserMax(exepath=str(tmpfile(dirname='bad_filename_dir', 
                                     filename='bad_filename_file')))
    with pytest.raises(ValueError):
        UserMax(exepath='path_does_not_exist')


rev_chron_versionyears = sorted(UserMax.supported_version_years, reverse=True)
@pytest.mark.parametrize('fake_installed_versions, req_year, exception', 
                        [([], None, RuntimeError),
                         ([], 14, KeyError),
                         ([], 2018, KeyError),
                         ([2015], 2016, KeyError),
                         ([2015], None, None),
                         ([2018, 2016], 2016, None),
                         ([2013, 2014, 2015, 2016], 16, None),
                         ([2014, 2015, 2016], None, None),
                         (rev_chron_versionyears,
                          rev_chron_versionyears[-1], None)])
def test_UserMax_init_with_year(fake_installed_versions, req_year, exception,
                            patch_max_root_env_vars, monkeypatch, tmpdir):
    """Test that expected exception is raised or if success is expected check that path attributes exist.class"""
    patch_max_root_env_vars(fake_installed_versions)
    if exception:
        with pytest.raises(exception) as e:
            UserMax(versionyear=req_year)
    else:
        usermax = UserMax(versionyear=req_year)
        expected_year = str(req_year if None else fake_installed_versions[-1])
        assert os.path.basename(usermax.root) == expected_year
        assert os.path.exists(usermax.exe)
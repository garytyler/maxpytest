from __future__ import print_function
import os
import pytest
import subprocess as sp
from maxpytest import callscript_testcaller

# TODO def imported_pytest_is_from_maxpytest_sitepkgs_if_not_avail_in_added
# TODO def imported_pytest_is_from_added_sitepkgs_if_avail_in_added


@pytest.fixture(scope="module")
def tempcwd(tmpdir_factory):
    return str(tmpdir_factory.mktemp("cwd"))


@pytest.fixture(scope="class")
def mock_cwd(tempcwd):
    """Create a mock virtual environment to use as source project for testing
    testcaller script
    """

    def run_command(command, cwd):
        return sp.Popen(command, cwd=cwd, stdout=sp.PIPE, stderr=sp.STDOUT)

    def _setup():
        try:
            _process = run_command(r"pipenv --python 2.7 install", tempcwd)
        except:
            _teardown()
            raise
        else:
            _process.wait()
            return _process

    def _teardown():
        try:
            _process = run_command(r"pipenv --rm", tempcwd)
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
def testcaller(mocker):
    """Patch testcaller attributes required for call_tests to run()"""
    mocker.patch.object(callscript_testcaller, "patch_isatty")
    mocker.patch.object(callscript_testcaller.os, "chdir")
    yield callscript_testcaller


class TestExpectedCalls(object):
    def test_patch_isatty(self, testcaller, mock_cwd):
        testcaller.prep_environment(cwd=mock_cwd)
        testcaller.patch_isatty.assert_called_once_with()

    def test_os_chdir(self, testcaller, mock_cwd):
        testcaller.prep_environment(cwd=mock_cwd)
        testcaller.os.chdir.assert_called_once_with(mock_cwd)


expand_combo_args_params = [
    (["-abc"], ["-a", "-b", "-c"]),
    (["--abc"], ["--abc"]),
    (["---abc"], ["---abc"]),
    (["-xzxz"], ["-x", "-z", "-x", "-z"]),
    (["--xz"], ["--xz"]),
    (
        ["-abc", "--abc", "---abc", "-xzxz", "--xz"],
        ["-a", "-b", "-c", "--abc", "---abc", "-x", "-z", "-x", "-z", "--xz"],
    ),
    (["--key=val"], ["--key=val"]),
    (["-key"], ["-k", "-e", "-y"]),
    (["key-"], ["key-"]),
    (["-key=val"], ["-key=val"]),
    (
        ["--key=val", "-key", "key-", "-key=val"],
        ["--key=val", "-k", "-e", "-y", "key-", "-key=val"],
    ),
    (["---qwert"], ["---qwert"]),
    (["-qwertqwert"], ["-q", "-w", "-e", "-r", "-t", "-q", "-w", "-e", "-r", "-t"]),
    (
        ["---qwert", "-qwertqwert"],
        ["---qwert", "-q", "-w", "-e", "-r", "-t", "-q", "-w", "-e", "-r", "-t"],
    ),
]


@pytest.mark.parametrize("arglist, result", expand_combo_args_params)
def test_expand_combo_args(arglist, result):
    assert result == callscript_testcaller.expand_combo_args(arglist)


@pytest.mark.parametrize(
    "arglist, result",
    [tuple([p[0], p[1] + ["--capture=sys"]]) for p in expand_combo_args_params],
)
def test_handle_pytest_args_add_capture_if_none(arglist, result):
    assert result == callscript_testcaller.handle_pytest_args(arglist)


@pytest.mark.parametrize(
    "arglist, result",
    [
        tuple([p[0] + ["--capture=fd"], p[1] + ["--capture=sys"]])
        for p in expand_combo_args_params
    ],
)
def test_handle_pytest_args_remove_bad_args(arglist, result):
    assert result == callscript_testcaller.handle_pytest_args(arglist)


@pytest.mark.parametrize(
    "arglist, result",
    [
        (["-sv"], ["-s", "-v"]),
        (["--verbose", "--capture=no"], ["--verbose", "--capture=no"]),
    ],
)
def test_handle_pytest_args_ignore_nocap_args(arglist, result):
    assert result == callscript_testcaller.handle_pytest_args(arglist)

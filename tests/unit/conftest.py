from __future__ import print_function
import pytest


@pytest.fixture(autouse=True)
def set_all_max_root_env_vars_to_blank(patch_max_root_env_vars):
    patch_max_root_env_vars([])


@pytest.fixture(autouse=True)
def temp_callscripts_dir(monkeypatch, tmpdir):
    from maxpytest import callscripts

    _callscriptsdir = str(tmpdir.mkdir("callscripts"))

    def callscriptsdir_callable():
        return _callscriptsdir

    monkeypatch.setattr(callscripts.tempfile, "gettempdir", callscriptsdir_callable)
    yield _callscriptsdir


@pytest.fixture
def patch_max_root_env_vars(monkeypatch, tmpdir):
    """Factory to patch proprietary 3ds Max environment vars with mock paths
    for each int in 'fake_installed_versions. Dirnames are version year and
    filenames are """
    from maxpytest.maxcom import UserMax

    def _patch_max_root_env_vars(fake_installed_versions):
        for year in UserMax.supported_version_years:
            var = "ADSK_3DSMAX_X64_{0}".format(str(year))
            if int(year) in fake_installed_versions:
                root_path = tmpdir.mkdir(str(year))
                exepath = root_path.join(UserMax.filename).write("content")
                monkeypatch.setenv(var, root_path)
            else:
                try:
                    monkeypatch.delenv(var)
                except KeyError:
                    pass

    yield _patch_max_root_env_vars


@pytest.fixture
def tmpfile(tmpdir):
    def _tmpfile(dirname, filename):
        _path = tmpdir.mkdir(dirname).join(filename)
        _path.write(filename)
        return _path

    yield _tmpfile


# mixedlist
mixedlist_params = [
    ["asd\fdfdfa0", r"3=--1234s", 2],
    [r"F:\\a;slkk46h"],
    [r"an2", 1234, "\61==", ["asdff"], "=1--34"],
]


@pytest.fixture(
    params=mixedlist_params,
    ids=["mixedlist" + str(n) for n in range(len(mixedlist_params))],
)
def mixedlist(request):
    yield request.param


# mixedstr
mixedstr_params = [r"asdfasdf", r"1jmcu5__^_@/$_\\av\n46", r"sd3k\r41\r234"]


@pytest.fixture(
    params=mixedstr_params,
    ids=["mixedstr" + str(n) for n in range(len(mixedstr_params))],
)
def mixedstr(request):
    yield request.param

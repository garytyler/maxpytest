from __future__ import print_function
import subprocess as sp
import os

try:
    import MaxPlus
    from pymxs import runtime as rt
except Exception as e:
    pass


def restart(scriptpath):
    maxrootdir = MaxPlus.PathManager.GetMaxSysRootDir()
    exepath = os.path.join(maxrootdir, r"3dsmax.exe")
    rt.checkForSave()
    sp.Popen(r'"{0}" -U PythonHost "{1}"'.format(exepath, scriptpath))
    rt.quitMAX(quiet=True)

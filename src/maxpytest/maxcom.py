#!/usr/bin/env python2
from __future__ import print_function
import os
import subprocess


class CommandExecutor(object):
    def __init__(self, exepath):
        if not exepath:
            self.exe = self._find_default_exepath()
            self.root = os.path.dirname(self.exe)
        elif self._matches_and_isfile(exepath):
            self.exe = exepath
            self.root = os.path.dirname(self.exe)
        else:
            raise ValueError(exepath)

    def _get_default_exepaths(self):
        raise NotImplementedError 

    def run_script(self):
        raise NotImplementedError 

    def _matches_and_isfile(self, exepath):
        if self.filename == os.path.basename(exepath):
            if os.path.isfile(exepath):
                return True
        return False

    def _find_default_exepath(self):
        for exepath in self._get_default_exepaths():
            if self._matches_and_isfile(exepath):
                return exepath
        raise RuntimeError('{0} installation not found.'.format(self.filename))

class MXSPyCOM(CommandExecutor):
    """
    exe - path to MXSPyCOM.exe
    """
    filename = 'MXSPyCOM.exe'
    def __init__(self, exepath=None):
        if not exepath:
            exepath = self._find_default_exepath()
        CommandExecutor.__init__(self, exepath=exepath)

    def _get_default_exepaths(self):
        progfiles = os.environ['PROGRAMFILES']
        default_path = os.path.join(progfiles, 'MXSPyCOM', 'MXSPyCOM.exe')
        return [default_path]

    def run_script(self, scriptpath):    
        command = r'"{0}" -s "{1}"'.format(self.exe, scriptpath)
        subprocess.Popen(command, shell=True)
        
class UserMax(CommandExecutor):
    """Retrieve/store path data about targeted 3ds Max installation and launching with launch scripts
    """
    filename = '3dsmax.exe'
    supported_version_years = list(range(2012, 2019 +1))
    def __init__(self, versionyear=None, exepath=None):
        if all([exepath, versionyear]):
            msg = self.__name__, 'accepts either year or exe as args, not both'
            raise ValueError(msg)
        elif versionyear:
            _root = self._get_max_root(versionyear)
            exepath = os.path.join(_root, self.filename)
        CommandExecutor.__init__(self, exepath=exepath)

    def run_script(self, scriptpath):
        command = '\"{0}\" -U PythonHost \"{1}\"'.format(self.exe, scriptpath)
        proc = subprocess.Popen(command, shell=True)

    def _get_full_year(self, partial_year):
        partial_year_str = str(partial_year)
        for full_year in self.supported_version_years[::-1]:
            if str(full_year).endswith(partial_year_str):
                return full_year

    def _get_max_root_env_var(self, year):
        return 'ADSK_3DSMAX_X64_{0}'.format(str(year))

    def _get_max_root(self, year):
        if len(str(year)) < 4:
            year = self._get_full_year(partial_year=year)
        return os.environ[self._get_max_root_env_var(year)]

    def _get_default_exepaths(self):
        """Returns environment variable, root path of executable of latest 3ds 
        Max version installed."""
        default_paths = []
        for year in self.supported_version_years[::-1]:
            try:
                root = os.environ[self._get_max_root_env_var(year)]
            except KeyError:
                continue
            else:
                exe = os.path.join(root, self.filename)
                default_paths.append(exe)
        return default_paths
# encoding: utf-8

import os
import sys

from cx_Freeze import setup, Executable

import versioninfo

name        = versioninfo.name
version     = versioninfo.version
description = versioninfo.description

projpath            = '.'
base                = 'Win32GUI'
icon_path           = 'app.ico'
entrypoint_filename = '{}.py'.format(name)

sys.path.append(os.path.abspath(projpath))

# http://cx-freeze.readthedocs.io/en/latest/distutils.html#build-exe
outdir   = 'dist_{:}'.format(name)
includes = []
excludes = []
packages = []
include_files = [
    os.environ['TCL_DLL_PATH'],
    os.environ['TK_DLL_PATH'],
]
options = {
    'build_exe': {
        'build_exe': outdir,
        'includes' : includes,
        'excludes' : excludes,
        'packages' : packages,
        'include_files' : include_files,
    },
}

# http://cx-freeze.readthedocs.io/en/latest/distutils.html#cx-freeze-executable
entrypoint_fullpath = os.path.abspath(entrypoint_filename)
executables = [
    Executable(entrypoint_fullpath, base=base, icon=icon_path)
]

setup(
    name        = name,
    version     = version,
    description = description,
    options     = options,
    executables = executables
)

@echo off
setlocal

set DIST_ROOT_NAME=dist_incl
set DIST_ROOT_PATH=%~dp0dist_incl
set DIST_LIB_PATH=%DIST_ROOT_PATH%\lib
set REMOVE_FOLDER_CMD=rmdir /s /q

rem Remove unneed folders for reducing size.
%REMOVE_FOLDER_CMD% %DIST_ROOT_PATH%\tk\demos
%REMOVE_FOLDER_CMD% %DIST_ROOT_PATH%\tk\images
%REMOVE_FOLDER_CMD% %DIST_ROOT_PATH%\tk\msgs
%REMOVE_FOLDER_CMD% %DIST_ROOT_PATH%\tcl\encoding
%REMOVE_FOLDER_CMD% %DIST_ROOT_PATH%\tcl\http1.0
%REMOVE_FOLDER_CMD% %DIST_ROOT_PATH%\tcl\msgs
%REMOVE_FOLDER_CMD% %DIST_ROOT_PATH%\tcl\opt0.4
%REMOVE_FOLDER_CMD% %DIST_ROOT_PATH%\tcl\tzdata

rem Move Dlls to lib directory for avoiding 'ImportError: DLL load failed.'.
rem But do remove about duplicated at first.
del %DIST_ROOT_PATH%\python36.dll
del %DIST_ROOT_PATH%\VCRUNTIME140.dll
move %DIST_ROOT_PATH%\*.dll %DIST_LIB_PATH%

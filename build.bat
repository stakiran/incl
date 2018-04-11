@echo off

call "%~dp0build_preferences.bat"

python "%~dp0build.py" build

call "%~dp0build_postproc.bat"

exit /b

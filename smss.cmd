@echo off
pushd "%~dp0"
chcp 65001>nul
set BASEPATH=%~dp0
set BASEPATH=%BASEPATH:~0,-1%

set PYTHONURL=https://www.python.org/ftp/python/3.9.2/python-3.9.2-embed-amd64.zip
set PYTHONDIR=%BASEPATH%/python
set PYTHONBIN=%PYTHONDIR%/python.exe
set TEMPDIR=%BASEPATH%/temp
goto :pythonCheck

:pythonCheck
if exist "%PYTHONBIN%" goto :runScript
if not exist "%TEMPDIR%" (
  md "%TEMPDIR%"
)
curl -L %PYTHONURL% -o "%TEMPDIR%/python.zip"
powershell Expand-Archive -LiteralPath '%TEMPDIR%/python.zip' -DestinationPath '%PYTHONDIR%'
goto :runScript

:runScript
"%PYTHONBIN%" .\smss-core.py
goto :end

:end
pause
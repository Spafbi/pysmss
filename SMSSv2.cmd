@echo off
pushd "%~dp0"
chcp 65001>nul
set BASEPATH=%~dp0
set BASEPATH=%BASEPATH:~0,-1%

if NOT "%BASEPATH%"=="%BASEPATH: =%" goto :noSpaces

set PYTHONURL=https://www.python.org/ftp/python/3.9.2/python-3.9.2-embed-amd64.zip
set PYTHONDIR=%BASEPATH%\python
set PYTHONBIN=%PYTHONDIR%\python.exe
set PIPBIN=%PYTHONDIR%\Scripts\pip.exe
set PIPURL=https://bootstrap.pypa.io/get-pip.py
set SMSSTEMP=%BASEPATH%\temp
goto update

:update
echo Checking for new Simplified Miscreated Server Script updates...
set GITURL=https://api.github.com/repos/Spafbi/pysmss/releases/latest
set DOWNLOADURL=https://github.com/Spafbi/pysmss/releases/download/
set CORESCRIPT=SMSSv2.py
set DOWNLOAD=0
powershell -Command "$request=${env:GITURL}; [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Write-Output (Invoke-WebRequest -UseBasicParsing $request |ConvertFrom-Json |Select tag_name -ExpandProperty tag_name)">latest_release


REM This if statement exists so I don't overwrite the core script while developing
if exist .\.git\ (
  set TARGETSCRIPT=SMSSv2_download.py
) else (
  set TARGETSCRIPT=%CORESCRIPT%
)

if exist "local_release" (
  set /p CURRENT=<local_release
) else (
  set CURRENT=0
)

if exist "latest_release" (
  set /p LATEST=<latest_release
) else (
  set LATEST=0
)

if "%LATEST%" == "0" if "%CURRENT%" == "0" (
  echo No python script exists and the current release for download cannot be determined at this time.
  echo No action taken.
  call end
)

if not exist %TARGETSCRIPT% set DOWNLOAD=1
if "%CURRENT%" == "0" set DOWNLOAD=1
if not "%CURRENT%" == "%LATEST%" set DOWNLOAD=1
if "%DOWNLOAD%" == "1" (
  curl -L "%DOWNLOADURL%%LATEST%/%CORESCRIPT%">%TARGETSCRIPT%
  echo %LATEST%>local_release
)
goto :pythonCheck

:pythonCheck
if exist "%PYTHONBIN%" goto :importSite
echo Downloading and installing embedded Python...
if not exist "%SMSSTEMP%" (
  md "%SMSSTEMP%"
)
curl -L %PYTHONURL% -o "%SMSSTEMP%/python.zip"
powershell Expand-Archive -LiteralPath '%SMSSTEMP%/python.zip' -DestinationPath '%PYTHONDIR%'
goto :importSite

:importSite
setlocal
>%PYTHONDIR%\python39._pth (
    for %%I in (
        "python39.zip"
        "."
        ""
        "import site"
    ) do echo %%~I
)
goto :pipCheck

:pipCheck
if exist "%PIPBIN%" goto :moduleCheck
echo Setting up Python pip...
curl -L %PIPURL% -o "%SMSSTEMP%/get-pip.py"
"%PYTHONBIN%" "%SMSSTEMP%/get-pip.py" --no-warn-script-location
goto :moduleCheck

:moduleCheck
echo Validating support modules...
for %%x in (bs4 colorama requests) do (
  "%PYTHONBIN%" -m pip install -q -U %%x --no-warn-script-location
)
goto :runScript

:runScript
"%PYTHONBIN%" %CORESCRIPT%
if exist "%BASEPATH%\stop" goto :stopScript
if exist "%BASEPATH%\stop.txt" goto :stopScript
goto :update

:stopScript
echo Stop file exists. Remove the stop file if you wish to allow the server to
echo automatically restart
goto :end

:noSpaces
echo This script cannot be run from a path having spaces.
echo     %BASEPATH%
goto :end

:end
pause
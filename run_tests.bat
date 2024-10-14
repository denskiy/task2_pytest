@echo off
setlocal

REM Activate the Python virtual environment
echo Activating Python virtual environment...
call C:\ProgramData\Jenkins\.jenkins\workspace\PytestPipeline\venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo Failed to activate virtual environment.
    exit /b %errorlevel%
)

REM Change directory to your tests folder (if necessary)
echo Changing to tests directory...
cd C:\ProgramData\Jenkins\.jenkins\workspace\PytestPipeline
if %errorlevel% neq 0 (
    echo Failed to change directory.
    exit /b %errorlevel%
)

echo Installing required Python packages...
pip install -r requirements.txt

echo Running pytest...
pytest
if %errorlevel% neq 0 (
    echo Pytest failed.
    exit /b %errorlevel%
) else (
    echo Pytest completed successfully.
)

REM Deactivate virtual environment
echo Deactivating virtual environment...
call deactivate
if %errorlevel% neq 0 (
    echo Failed to deactivate virtual environment.
    exit /b %errorlevel%
)

echo Script finished.
endlocal
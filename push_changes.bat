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
echo Changing directory...
cd %~2
if %errorlevel% neq 0 (
    echo Failed to change directory.
    exit /b %errorlevel%
)

REM Configure Git user for local repository
git config user.email "denskiy17@gmail.com"
git config user.name "denskiy"

REM Check if the branch exists
git rev-parse --verify release-new
IF %ERRORLEVEL% equ 0 (
    ECHO Switching to existing branch 'release-new'
    git checkout release-new
) ELSE (
    ECHO Creating new branch 'release-new'
    git checkout -b release-new
)
IF %ERRORLEVEL% neq 0 exit /b %ERRORLEVEL%

@REM REM Synchronize files excluding .git directory
@REM robocopy ../ ./ /MIR /XD .git
@REM if %ERRORLEVEL% leq 7 (
@REM     echo Success or minor errors detected, continuing...
@REM ) else (
@REM     echo Error during directory synchronization
@REM     exit /b %ERRORLEVEL%
@REM )

REM Stage files, commit and push new branch
git add .
git commit -m "Deploying code to release branch"
git push --set-upstream origin release-new
if %ERRORLEVEL% neq 0 (
    echo Error in deployment script
    exit /b %ERRORLEVEL%
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
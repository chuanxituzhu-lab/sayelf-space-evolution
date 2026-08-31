@echo off
chcp 65001 >nul
cd /d "%~dp0"
where py >nul 2>nul
if %errorlevel%==0 (
  py app.py
  goto :eof
)
where python >nul 2>nul
if %errorlevel%==0 (
  python app.py
  goto :eof
)
echo.
echo [Sayelf Space Evolution] 未检测到 Python 3。
echo 请先安装 Python 3.10+，安装时勾选 Add Python to PATH。
echo 安装完成后重新双击 start_windows.bat。
echo.
pause

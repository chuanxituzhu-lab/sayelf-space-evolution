Set-Location $PSScriptRoot
if (Get-Command py -ErrorAction SilentlyContinue) { py app.py; exit }
if (Get-Command python -ErrorAction SilentlyContinue) { python app.py; exit }
Write-Host "未检测到 Python 3.10+。请安装 Python 后重试。"
Read-Host "按回车退出"

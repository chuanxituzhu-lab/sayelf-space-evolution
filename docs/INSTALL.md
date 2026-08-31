# 安装说明

## Windows
要求：Python 3.10+。

1. 解压 ZIP。
2. 不要只把 `start_windows.bat` 单独拖到桌面，必须保留整个目录结构。
3. 双击 `start_windows.bat`。
4. 首次启动时如果 Windows 防火墙询问，只需允许本机私有网络；程序仅监听 `127.0.0.1`。

## 常见问题
### 双击后闪退
在文件夹空白处打开 PowerShell，运行：
```powershell
py app.py
```
查看报错。

### 提示没有 Python
安装 Python 3.10+，并勾选 Add Python to PATH。

### 端口被占用
PowerShell：
```powershell
$env:SPACE_EVOLUTION_PORT=8877
py app.py
```
然后访问 `http://127.0.0.1:8877/`。

### 数据保存在哪里
项目配置默认保存在当前浏览器的 LocalStorage 中；通过「导出项目 .json」可以做独立备份。

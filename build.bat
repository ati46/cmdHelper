@echo off

IF NOT EXIST "venv" (
    python -m venv venv
)
call venv\Scripts\activate.bat

pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
pyinstaller -F -w --name cmd_helper main.py
echo Build finished! Check the 'dist' directory for 'cmd_helper.exe'.
pause

#!/bin/bash

if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

source venv/bin/activate

./venv/bin/pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
./venv/bin/pyinstaller -F -w --name cmd_helper main.py
echo "Build finished! Check the 'dist' directory for 'cmd_helper' binary."

#!/bin/bash
cd "$(dirname "$0")"

# 如果不存在虚拟环境，则创建它
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# 激活虚拟环境
source venv/bin/activate

# 使用 sentinel 机制，仅当 requirements.txt 被更新时才运行 pip install
SENTINEL="venv/sentinel"
if [ ! -f "$SENTINEL" ] || [ "requirements.txt" -nt "$SENTINEL" ]; then
    ./venv/bin/pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
    touch "$SENTINEL"
fi

nohup ./venv/bin/python main.py >/dev/null 2>&1 &

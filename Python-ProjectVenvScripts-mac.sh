#!/bin/bash

# 加载 conda 配置文件，确保能够激活环境
source /opt/anaconda3/etc/profile.d/conda.sh

# 激活 Conda 环境
conda activate py310-venv_20240405_140626

# 运行 Python 脚本
python App.py

# 退出 Conda 环境
conda deactivate

# 暂停脚本执行，等待用户按任意键继续
read -p "Press any key to continue..."

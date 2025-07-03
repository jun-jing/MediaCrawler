#!/bin/bash

# 加载 conda 配置文件，确保能够执行 conda 命令
source /opt/anaconda3/etc/profile.d/conda.sh

# 删除指定的 Conda 环境
conda env remove --name py310-venv_20240405_140626

# 确认环境已被成功删除
conda env list

# 暂停脚本执行，等待用户按任意键继续
read -p "Press any key to continue..."

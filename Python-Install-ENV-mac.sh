#!/bin/bash

# Ensure that conda is initialized in the script
source /opt/anaconda3/etc/profile.d/conda.sh

# 激活 Conda 环境
conda activate py310-venv_20240405_140626

# 安装 requirements.txt 中的依赖
pip install -r Python-Requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple 

# 如果需要安装额外的包，解除以下注释并替换为实际包名
# pip install your_required_package

# 或者使用 Conda 安装其他必要的包，解除以下注释并替换为实际包名
# conda install your_required_package

# 查看已安装的包
conda list

# 退出 Conda 环境
conda deactivate

# 暂停脚本，等待用户按任意键继续
read -p "Press any key to continue..."

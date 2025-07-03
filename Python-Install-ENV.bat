@echo off

REM 激活您的 Conda 环境，py310默认环境，横杠之后接上获取的venv和时间日期时分秒
call conda activate py310-venv_20240405_140626

REM 如果需要安装 pip 包，可以使用以下命令：
pip install -r Python-Requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple 

REM 如果需要安装 pip 包，可以使用以下命令：
REM pip install your_required_package
REM 如果pip 包，不成功可以试试以下命令：
REM call conda install your_required_package

REM 确认安装成功
call conda list

REM 关闭环境
call conda deactivate

PAUSE
@echo off
REM 激活您的 Conda 环境，py310默认环境，横杠之后接上获取的venv和时间日期时分秒
call conda activate py310-venv_20240405_140626

REM 运行 Python 脚本
python Python-Project.py

REM 关闭 Conda 环境
call conda deactivate

PAUSE
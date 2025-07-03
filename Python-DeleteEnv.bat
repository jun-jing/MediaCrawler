@echo off
REM 创建您的 Conda 虚拟环境
call conda env remove --name py310-venv_20240405_140626

REM 确认环境是否已经删除成功
call conda env list

PAUSE


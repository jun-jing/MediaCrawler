@echo off
REM 创建您的 Conda 虚拟环境
call conda create -n py310-venv_20240405_140626 python=3.10

REM 确认安装成功，似乎上面的安装成功之后就会直接退出，下面的内容无效了
call conda list

PAUSE


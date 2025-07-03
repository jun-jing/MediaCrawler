@echo off

REM �������� Conda ������py310Ĭ�ϻ��������֮����ϻ�ȡ��venv��ʱ������ʱ����
call conda activate py396-venv_20250703_115623-MediaCrawler

REM �����Ҫ��װ pip ��������ʹ���������
pip install -r Python-Requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple 

REM �����Ҫ��װ pip ��������ʹ���������
REM pip install your_required_package
REM ���pip �������ɹ����������������
REM call conda install your_required_package

REM ȷ�ϰ�װ�ɹ�
call conda list

REM �رջ���
call conda deactivate

PAUSE
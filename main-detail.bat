@echo off
REM �������� Conda ������py310Ĭ�ϻ��������֮����ϻ�ȡ��venv��ʱ������ʱ����
call conda activate py396-venv_20250703_115623-MediaCrawler

REM ���� Python �ű�
python main.py --platform xhs --lt qrcode --type detail

REM �ر� Conda ����
call conda deactivate

PAUSE
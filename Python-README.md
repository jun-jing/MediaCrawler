# 注意事项

## 重要步骤

* 修改venv库名称 结合当前时分秒
* 装好了pip的库之后，直接导出到Python-Requirements.txt就可以直接给别人去用了

## 注释

Python-Folder_Create_And_Start
创建文件夹把所有文件都丢进去

Python-OneKey
创建虚拟环境，记得要call
然后等待安装install库

Python-Requirements
把需要的库提前写入，记得控制版本号，方便待会一次性安装

Python-Install-ENV
激活环境之后，安装需要的库
有可能需要pip install和conda install来安装
之后可能需要用pip freeze 把内容保存到本地来使用

Python-Project
等待执行的py文件

Python-ProjectVenvScripts
用来在当前环境下面执行python代码的脚本

Python-README
介绍文档

.gitignore
补充上当前文件夹需要忽略的内容, 以免占用太多资源

## 代码功能介绍

### 切换到 main 分支并更新
先在平台上点击sync fork

git checkout main
git pull origin main

### 切回自己的开发分支
git checkout my-feature

### 合并 main 的更新进来
git merge main

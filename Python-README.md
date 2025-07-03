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

### 命令行功能介绍

当然可以，以下是这个命令行工具的帮助信息（Help 文档）的**中文翻译与解释**：

---

# 📦 **媒体爬虫程序（Media crawler program）帮助说明翻译**

## 🎯 程序用途

这是一个媒体平台的爬虫程序，支持多个平台，可指定爬取内容、登录方式、保存方式等参数。

---

## 🧩 可选参数说明（optional arguments）

| 参数                   | 类型           | 说明                                                                                           |
| -------------------- | ------------ | -------------------------------------------------------------------------------------------- |
| `-h`, `--help`       | 命令           | 显示帮助信息并退出程序                                                                                  |
| `--platform`         | 选项（必须从中选择一个） | 选择要爬取的平台，支持：<br>`xhs`（小红书）、`dy`（抖音）、`ks`（快手）、`bili`（哔哩哔哩）、`wb`（微博）、`tieba`（百度贴吧）、`zhihu`（知乎） |
| `--lt`               | 登录方式         | 登录类型，支持：<br>`qrcode`（扫码登录）<br>`phone`（手机号登录）<br>`cookie`（使用 Cookie 登录）                       |
| `--type`             | 爬虫类型         | 要进行的操作类型：<br>`search`（搜索内容）<br>`detail`（爬取详情）<br>`creator`（创作者主页信息）                          |
| `--start`            | 数值           | 从第几页开始爬取（分页起始页码）                                                                             |
| `--keywords`         | 字符串          | 要搜索的关键词                                                                                      |
| `--get_comment`      | 布尔           | 是否获取一级评论，支持值（不区分大小写）：<br>`yes`、`true`、`t`、`y`、`1` 表示是<br>`no`、`false`、`f`、`n`、`0` 表示否        |
| `--get_sub_comment`  | 布尔           | 是否获取二级评论，支持值同上                                                                               |
| `--save_data_option` | 存储方式         | 数据保存方式，支持：<br>`csv`（保存为 CSV 文件）<br>`db`（保存到数据库）<br>`json`（保存为 JSON 文件）                       |
| `--cookies`          | 字符串          | 如果选择 cookie 登录方式，需要传入 cookie 字符串                                                             |

---

## 🛠 示例命令（举例）

```bash
python main.py --platform xhs --lt cookie --type search --start 1 --keywords "ChatGPT" --get_comment yes --get_sub_comment no --save_data_option csv --cookies "your_cookie_here"
```

这个命令表示：

* 平台：小红书（xhs）
* 登录方式：使用 cookie 登录
* 操作类型：搜索内容
* 从第 1 页开始
* 搜索关键词为 "ChatGPT"
* 获取一级评论，不获取二级评论
* 保存为 CSV 格式
* 使用指定的 cookie 字符串

---

需要我帮你构造一个完整命令，或者分析这个爬虫结构/源码也可以告诉我！


### 切换到 main 分支并更新
先在平台上点击sync fork

git checkout main
git pull origin main         # 拉取最新的 main

git checkout my-feature
git merge main               # 合并更新进来
git push origin my-feature  # 推送到自己的 GitHub
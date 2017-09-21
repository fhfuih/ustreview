# UST Review

## 简介 Overview

一个简单的练手爬虫，用于查询HKUST教授的评价。数据来源为[UST Space](https://ust.space)网站的Course Review。

A simple spider used to enquire about the reviews of professors in HKUST. Data is captured from 'Course Review' at [UST Space](https://ust.space).

## 开发环境 Requirement

Python 3.5

`pip install selenium`

`pip install bs4`

如果需要运行程序，请确保已经下载了至少一个WebDriver且加入了环境变量。程序调用WebDriver的规则如下：

If you wish to run the program on your computer, please ensure that at least one WebDriver has been downloaded and added to `PATH`. The rule it follows to choose WebDriver is shown below:

| First flag              | WebDriver |
| ----------------------- | --------- |
| `--debug` or `--chrome` | Chrome    |
| `--firefox`             | Firefox   |
| Other or none           | PhantomJS |





若要打包分发，则还需要

In case of distribution, you may also need

`pip install pyinstaller`

只需执行

You only need to run command

`pyinstaller cli.py`

## TODO

* 访问过于频繁会触发reCaptcha
* 解析js以代替Selenium提高速度
* 图形界面



* Frequent visits will trigger reCaptcha
* Replace Selenium with JS parsing to improve speed
* GUI

## 许可 License

![WTFPL](http://www.wtfpl.net/wp-content/uploads/2012/12/wtfpl-badge-4.png)

软件图标修改自作品[Professor by Saeful Muslim from the Noun Project](https://thenounproject.com/term/professor/1171625)。原作品采用[知识共享署名 3.0 美国许可协议](https://creativecommons.org/licenses/by/3.0/us/deed.zh)发布。

The software icon is derived from [Professor by Saeful Muslim from the Noun Project](https://thenounproject.com/term/professor/1171625). The original work is licensed under [Creative Commons Attribution 3.0 United States License](http://creativecommons.org/licenses/by/3.0/us/)

本软件作为个人制作的第三方软件，并非附属于香港科技大学、[UST Space](https://ust.space)网站或者任何其它组织、团队。

This software is a third-party software, and is not affiliated to HKUST, [UST Space](https://ust.space) website or any other organization or group.

本软件分发时所附带的`phantomjs.exe`为未经修改的PhantomJS二进制分发文件，其许可原文将会附在其他文件中。

The `phantomjs.exe` file that is included in the distribution is an unmodified copy of PhantomJS binary distribution. Its license will be specified in another file.
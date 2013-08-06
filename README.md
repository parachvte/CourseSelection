CourseSelection
==========

by Ryan, 8/6/2013

A python script used for [course selection(?) of Fudan University](http://xk.fudan.edu.cn/xk), so called "刷课机"

周日的时候，猥栋在用java写刷课机，于是手痒也写个来玩。

周日晚上熟悉了一下python的httplib模块，可以通过httplib发送POST和GET请求，写出可以手动输入验证码的刷课机，测试了一个python的验证码模块，大概叫pytesser之类的，效果不佳。

周一晚上试着自己提取验证码的特征码（他们是这么叫的吧0.0），手动输入验证正确的就当作特征码（attribute code），存下来。下次再碰到这个特征码，通过查表即可得到正确的数字或字母。

Performance
----------

测试可选课成功，每0.2秒尝试登录选课系统，进入系统后每3秒尝试选一门课（这是2012年某学期系统加入的新“特性”所致，当然有一个bug可以避免等待，不过写这个脚本只是玩玩的，应该不会有人真的用吧...就不要追求太多了嘛:）

连续2000组验证码连续验证正确，不过有的时候偶尔会抛个异常，猜测是网络的问题

P.S. 验证码的字符集不是想当然的[0-9a-z]，而是其中的不到20个字符，不知道写验证码的人怎么想的...

Shortage
----------

- 上面提到了，就是3秒的等待时间，这个太懒了应该不改进了
- 没有UI，虽然这个算不上缺点
- 如果选课失败，只是简单返回个NO，并不具体分析返回的具体原因从而做规则的优化。举个例子，如果一个课选满了，选课失败返回说(40/40)，但是本程序只知道是失败了，于是会不断鬼打墙一直尝试选这个课

How To Use
----------

如果你是python 2+的用户，运行：

    python CourseSelection.py

如果程序是给不会coding的人用（比如说用来把学妹用...），那么装上[py2exe](http://www.py2exe.org/)包，运行：

    python setup.py py2exe

然后把 `attribute_codes.txt` 放到dist文件夹内，dist即是一个可发行版本， `CourseSelection.exe` 为程序本体。

Files Structure
----------

- `CourseSelection.py`          程序本体，用来刷课
- `OCR.py`                      OCR，用来辨识验证码，存取特征码
- `attribute_codes.txt`         存取特征码的文件
- `setup.py`                    py2exe的setup文件
- `training.py`                 训练用，辅助生成特征码



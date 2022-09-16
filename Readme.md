# 南科大润杨羽毛球场地预定脚本

## 使用前
确保在`post.json`文件中修改相应信息，包括预定的学号，预定的起始时间，预定的人数，设定的抢场地时间
## 使用时
固定时间模式：为脚本设定一个运行时间，一般在晚上12点会有空场地放出，故`post.json`中`set_time`一般设置为`20XX-XX-XX 00:00:00`，脚本会在设定时间前5s开抢
```shell
# 固定时间模式运行
python script.py 0
```
手动回车模式：回车一次，自动在10个场地中寻找空闲位
```shell
# 手动回车模式运行
python script.py 1
```
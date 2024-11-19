# tools

找审稿人的脚本


## 提前说明

所有操作都在latest_tab上进行


## 流程
1. 把目标论文传给chatgpt让他返回所有引用文献
```markdown
找到这篇论文的所有引用文献，并将这些引用文献以一条为一行放到一个txt文件中，返回给我

```

2. 拿到这个文件，放到工作目录中，在脚本中指定文件名，运行脚本（后期可能写成参数传递方式）


3. 脚本会打开浏览器，然后搜索引用文献，找到目标作者，写到execel文件中
4. 手动找到email，写到execel文件中

## 如果出现验证码错误 
处理验证码的操作还没有实际验证过，因为一直没有弹出验证码。

主要问题是什么？ 是担心再次出现浏览器点击然后验证，然后验证码不出现的情况。

上次主要怀疑是因为是直接使用python起的的浏览器。

如果再次遇到验证码出现但是点击后没有弹出的情况，可以尝试手动启动浏览器后，然后指定脚本使用已经启动的浏览器。

在mac上启动浏览器的命令是：

```shell
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222

```

然后在脚本中指定：

```python
from DrissionPage import Chromium, ChromiumOptions

# 创建配置对象（默认从 ini 文件中读取配置）
co = ChromiumOptions()

# 设置使用已经启动的浏览器
co.existing_only()

# 以该配置创建浏览器对象
chromium = Chromium(co)

```

### 其他
计划包含三个文件，作者txt，引用txt，关键词txt，一行一个。使用chatgpt完成数据读取，然后手动写入的这些txt中。
但我目前想，只需要一个引用txt就可以了，是否需要自动处理关键词和作者，待定。我想的是作者手动处理，然后引用不够，必须使用关键词，也是手动处理。这样就可以了。反正找email也必须手动处理。
我有考虑是否使用steamlit写一个web页面，然后做个交互，不过如果只是我自己使用的话，我想无所谓了。


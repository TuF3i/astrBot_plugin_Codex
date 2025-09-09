import base64

from astrbot.api import logger

class Commandexec():
    def __init__(self, client, image_name):
        self.image_name = image_name
        self.client = client
        self.help_doc = r'''
帮助文档：
------
Author: TuF3i
Version: 1.0.0-dev
Github: https://github.com/TuF3i/AstrBot_Codex
------
1.代码执行：
/code shell
<cmd>

/code python
<cmd>

/code java
<cmd>

/code C
<cmd>

2.命令黑名单：
/code add_acl <cmd>
#添加黑名单命令，此命令将不会被执行

/code del_acl <cmd>
#移除黑名单命令，此命令将会被执行

注意：
1.不要使用对系统有害的命令
2.程序会从第一个\n处开始分割代码，所以在/code <language>后一定要先回车再输命令
3.目前支持：Shell, Python, Java, C 四种语言
'''

    def code_exec_shell(self,cmd_raw):
        cmd = cmd_raw.split("\n", 1)
        cmd = cmd[1]
        encoded_script = base64.b64encode(cmd.encode('utf-8')).decode('utf-8')
        logger.info(f"cmd:{cmd}")
        res = base64.b64decode(self.client.containers.run(self.image_name, f"python3 /main.py shell {encoded_script}", remove=True))
        return res.decode('utf-8')

    def code_exec_python(self,cmd_raw):
        cmd = cmd_raw.split("\n", 1)
        cmd = cmd[1]
        encoded_script = base64.b64encode(cmd.encode('utf-8')).decode('utf-8')
        logger.info(f"cmd:{cmd}")
        res = base64.b64decode(self.client.containers.run(self.image_name, f"python3 /main.py python {encoded_script}", remove=True))
        return res.decode('utf-8')

    def code_exec_java(self,cmd_raw):
        cmd = cmd_raw.split("\n", 1)
        cmd = cmd[1]
        encoded_script = base64.b64encode(cmd.encode('utf-8')).decode('utf-8')
        logger.info(f"cmd:{cmd}")
        res = base64.b64decode(self.client.containers.run(self.image_name, f"python3 /main.py java {encoded_script}", remove=True))
        return res.decode('utf-8')

    def code_exec_C(self,cmd_raw):
        cmd = cmd_raw.split("\n", 1)
        cmd = cmd[1]
        encoded_script = base64.b64encode(cmd.encode('utf-8')).decode('utf-8')
        logger.info(f"cmd:{cmd}")
        res = base64.b64decode(self.client.containers.run(self.image_name, f"python3 /main.py C {encoded_script}", remove=True))
        return res.decode('utf-8')
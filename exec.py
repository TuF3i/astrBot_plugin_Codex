import base64
import asyncio

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

注意：
1.不要使用对系统有害的命令
2.程序会从第一个\n处开始分割代码，所以在/code <language>后一定要先回车再输命令
3.目前支持：Shell, Python, Java, C 四种语言
'''
    
    async def _execute_code(self, language, cmd_raw):
        cmd = cmd_raw.split("\n", 1)[1]
        encoded_script = base64.b64encode(cmd.encode('utf-8')).decode('utf-8')
        logger.info(f"cmd:{cmd}")
        
        try:
            # 创建容器配置
            container = await self.client.containers.create({
                'Image': self.image_name,
                'Cmd': ['python3', '/main.py', language, encoded_script],
                'NetworkDisabled': False
            })
            
            await container.start()     # 启动容器
            
            # 等待容器完成，设置超时
            try:
                await asyncio.wait_for(container.wait(), timeout=30)
            except asyncio.TimeoutError:
                logger.info(f"容器执行超时")
                await container.stop()
                return "容器执行超时"
            
            logs = await container.log(stdout=True, stderr=True)    # 获取容器日志
            
            await container.delete(force=True)  # 删除容器
            
            return logs.decode('utf-8')
        except Exception as e:
            logger.info(f"执行代码时发生错误: {e}")
            return f"执行错误: {str(e)}"
    
    async def code_exec_shell(self, cmd_raw):
        return await self._execute_code('shell', cmd_raw)
    
    async def code_exec_python(self, cmd_raw):
        return await self._execute_code('python', cmd_raw)
    
    async def code_exec_java(self, cmd_raw):
        return await self._execute_code('java', cmd_raw)
    
    async def code_exec_c(self, cmd_raw):
        return await self._execute_code('C', cmd_raw)
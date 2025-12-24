import base64
import asyncio
import re

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

    def _check_risk(self, code):
        # 简单的关键词黑名单，防止明显的恶意破坏
        # 注意：这不能替代沙箱隔离，只是第一道防线
        risk_patterns = [
            r":\(\)\s*\{\s*:\|:\s*&?\s*\}\s*;",  # Fork bomb
            r"rm\s+(-rf|-r|-f)\s+/*",            # rm -rf / (dangerous looking)
            r"mkfs",                              # Format disk
            r"dd\s+if=/dev/zero",                 # Disk fill
            r">\s*/dev/sd[a-z]",                  # Write to raw device
            r"chmod\s+(-R)?\s+777\s+/",           # Permission destruction
            r"wget|curl|nc|ping|ssh",             # Network tools (network is disabled anyway)
        ]
        
        for pattern in risk_patterns:
            if re.search(pattern, code, re.IGNORECASE):
                return True, f"检测到潜在的高风险命令 (匹配规则: {pattern})"
        return False, ""
    
    async def _execute_code(self, language, cmd_raw):
        parts = cmd_raw.split("\n", 1)
        if len(parts) < 2:
            return "格式错误：请在语言名称后换行输入代码。"
        cmd = parts[1]

        # 风险检查
        is_risky, risk_msg = self._check_risk(cmd)
        if is_risky:
            return f"执行被拒绝: {risk_msg}"

        encoded_script = base64.b64encode(cmd.encode('utf-8')).decode('utf-8')
        logger.info(f"cmd:{cmd}")
        
        try:
            # 创建容器配置
            container = await self.client.containers.create({
                'Image': self.image_name,
                'Cmd': ['python3', '/main.py', language, encoded_script],
                'NetworkDisabled': True, # 禁用网络
                'HostConfig': {
                    'Memory': 128 * 1024 * 1024,  # 限制内存 128MB
                    'NanoCpus': 500000000,        # 限制 CPU 0.5 核
                    'PidsLimit': 64,              # 限制进程数防止 Fork 炸弹
                    'CapDrop': ['ALL'],           # 移除所有 Linux Capabilities
                    'Privileged': False           # 确保非特权模式
                }
            })
            
            await container.start()     # 启动容器
            
            # 等待容器完成，设置超时
            try:
                await asyncio.wait_for(container.wait(), timeout=30)
            except asyncio.TimeoutError:
                logger.info(f"容器执行超时")
                await container.stop()
                return "容器执行超时"
            
            # 获取容器日志
            logs = await container.log(stdout=True, stderr=True)
            log_line = ''.join(logs)
            
            # 限制输出长度，防止刷屏
            if len(log_line) > 5000:
                log_line = log_line[:5000] + "\n... (输出过长，已截断)"

            await container.delete(force=True)  # 删除容器

            # 尝试清理日志输出中的空白字符
            log_line = log_line.strip()
            
            try:
                return base64.b64decode(log_line)
            except Exception as decode_error:
                logger.error(f"Base64 decode error. Raw output: {log_line}")
                return f"执行结果解码失败: {decode_error}. 原始输出: {log_line}"

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

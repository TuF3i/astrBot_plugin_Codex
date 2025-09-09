from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
import astrbot.api.message_components as Comp

from .exec import Commandexec
from .dockerSupport import dockerSupport

@register("AstrBot_pluggin_Codex", "TuF3i", "这是一个基于Docker的Linux命令执行插件。", "1.1.0")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    async def initialize(self):
        self.dockerEnv = dockerSupport(useXuanYuanMirror=False)  #使用镜像加速
        await self.dockerEnv.init_docker_env()
        await self.dockerEnv.check_images()

        self.exec = Commandexec(self.dockerEnv.client, self.dockerEnv.imageName)

    @filter.command_group("code")
    def code(self):
        pass

    @code.command("help")
    async def help(self,event: AstrMessageEvent):
        """获取帮助信息"""
        chain = [
            Comp.At(qq=event.get_sender_id()),
            Comp.Plain(self.exec.help_doc)
        ]
        yield event.chain_result(chain)

    @code.command("shell")
    async def shell_lan(self, event: AstrMessageEvent):
        """执行Shell代码"""
        logger.info(f"raw_message:{event.message_str}") # 平台下发的原始消息在这里
        res = await self.exec.code_exec_shell(event.message_str)
        yield event.plain_result(res)
    
    @code.command("python")
    async def python_lan(self, event: AstrMessageEvent):
        """执行Python代码"""
        logger.info(f"raw_message:{event.message_str}")
        res = await self.exec.code_exec_python(event.message_str)
        yield event.plain_result(res)

    @code.command("java")
    async def java_lan(self, event: AstrMessageEvent):
        """执行Java代码"""
        logger.info(f"raw_message:{event.message_str}")
        res = await self.exec.code_exec_java(event.message_str)
        yield event.plain_result(res)

    @code.command("C")
    async def C_lan(self, event: AstrMessageEvent):
        """执行C代码"""
        logger.info(f"raw_message:{event.message_str}")
        res = await self.exec.code_exec_c(event.message_str)
        yield event.plain_result(res)

    async def terminate(self):
        pass

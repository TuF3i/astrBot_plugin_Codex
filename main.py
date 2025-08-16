from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
import docker
import base64

@register("AstrBot_Codex", "TuF3i", "这是一个基于Docker的Linux命令执行插件。", "1.0")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    async def initialize(self):
        """可选择实现异步的插件初始化方法，当实例化该插件类之后会自动调用该方法。"""
        try:
            self.client = docker.DockerClient(base_url='unix:///var/run/docker.sock')
            logger.info(f"成功连接到 Docker 引擎 (API 版本: {self.client.api.version()['ApiVersion']})")
        except docker.errors.DockerException as e:
            logger.info(f"连接失败: {str(e)}")

    # 注册指令的装饰器。指令名为 helloworld。注册成功后，发送 `/helloworld` 就会触发这个指令，并回复 `你好, {user_name}!`
    @filter.command_group("code")
    def code(self):
        pass

    @code.command("sh")
    async def sh(self, event: AstrMessageEvent,):
        # /math add 1 2 -> 结果是: 3
        # res = yield self.client.containers.run("2ed9f0bd998d",f'''cat << 'EOF' > system_info.sh
        # {cmd}
        # EOF && chmod +x system_info.sh && ./system_info.sh''',remove=True)
        logger.info(f"raw_message:{event.message_str}") # 平台下发的原始消息在这里
        cmd = (event.message_str).split("\n", 1)
        cmd = cmd[1]
        encoded_script = base64.b64encode(cmd.encode('utf-8')).decode('utf-8')
        logger.info(f"cmd:{cmd}")
        res = base64.b64decode(self.client.containers.run("cd9c6f7a266f",f"python3 /main.py shell {encoded_script}",remove=True))
        url = await self.text_to_image(res.decode('utf-8'))
        yield event.image_result(url)

    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""

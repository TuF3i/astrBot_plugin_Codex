import asyncio

from astrbot.api import logger

import aiodocker

async def pull_docker_image(client, image_name):
    try:
        logger.info(f"正在拉取镜像: {image_name}")
        await client.images.pull(image_name)
        logger.info(f"镜像拉取成功: {image_name}")
        return True
    except Exception as e:
        logger.info(f"拉取镜像时发生错误: {e},请手动拉取镜像,详细信息请阅读README.md")
        return False

async def check_image_exists_locally(client, image_name):
    try:
        images = await client.images.list()
        for image in images:
            if image_name in image['RepoTags'] or f"{image_name}:latest" in image['RepoTags']:
                return True
        return False
    except Exception as e:
        logger.info(f"检查镜像时发生错误: {e}")
        return False

class dockerSupport():
    def __init__(self, useXuanYuanMirror):
        if useXuanYuanMirror:
            self.imageName = "docker.xuanyuan.me/tuf3i/code_exec"  # 使用镜像加速
        else:
            self.imageName = "tuf3i/code_exec"  #不使用镜像加速
        self.client = None

    async def init_docker_env(self):
        try:
            self.client = aiodocker.Docker()
            version = await self.client.version()
            logger.info(f"成功连接到 Docker 引擎 (API 版本: {version['ApiVersion']})"
            )
        except Exception as e:
            logger.info(f"连接失败: {str(e)}")

    async def check_images(self):
        logger.info("开始检测镜像信息")
        if self.client is None:
            logger.info("Docker客户端未初始化，跳过镜像检查")
            return
        
        if await check_image_exists_locally(self.client, self.imageName):
            logger.info(f"镜像<{self.imageName}>存在")
        else:
            logger.info(f"镜像<{self.imageName}>不存在，开始拉取镜像")
            await pull_docker_image(self.client, self.imageName)
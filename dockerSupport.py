import time

from astrbot.api import logger

import docker
from docker.errors import APIError, ImageNotFound

def pull_docker_image(client, image_name, auth_config):
    try:
        # 拉取镜像
        logger.info(f"正在拉取镜像: {image_name}")
        image = client.images.pull(image_name, auth_config=auth_config)

        logger.info(f"镜像拉取成功: {image.tags}")
        return image

    except APIError as e:
        logger.info(f"Docker API错误: {e}")
        return None
    except Exception as e:
        logger.info(f"拉取镜像时发生错误: {e}")
        return None

def check_image_exists_locally(client, image_name):
    try:
        client.images.get(image_name)
        return True
    except ImageNotFound:
        return False

class dockerSupport():
    def __init__(self,useXuanYuanMirror):
        if useXuanYuanMirror:
            self.imageName = "docker.xuanyuan.me/tuf3i/code_exec"  # 使用镜像加速
        else:
            self.imageName = "tuf3i/code_exec"  #不使用镜像加速
        self.auth_config = None
        self.docker_url = "unix:///var/run/docker.sock"

    def init_docker_env(self):
        try:
            self.client = docker.DockerClient(base_url=self.docker_url)
            logger.info(f"成功连接到 Docker 引擎 (API 版本: {self.client.api.version()['ApiVersion']})")
            time.sleep(1)
        except docker.errors.DockerException as e:
            logger.info(f"连接失败: {str(e)}")

    def check_images(self):
        logger.info("开始检测镜像信息")
        if check_image_exists_locally(self.client ,self.imageName):
            logger.info(f"镜像<{self.imageName}>存在")
        else:
            logger.info(f"镜像<{self.imageName}>不存在，开始拉取镜像")
            pull_docker_image(self.client, self.imageName, self.auth_config)
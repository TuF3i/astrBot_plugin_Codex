FROM python:3.11-slim

# 更换为国内源以加快构建速度 (Debian 12 / Bookworm)
RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list.d/debian.sources

# 安装 GCC (用于 C 语言) 和 OpenJDK (用于 Java)
RUN apt-get update && apt-get install -y \
    gcc \
    default-jdk \
    && rm -rf /var/lib/apt/lists/*

# 复制插件的核心执行脚本到镜像中
COPY exec/main.py /main.py

# 设置工作目录
WORKDIR /

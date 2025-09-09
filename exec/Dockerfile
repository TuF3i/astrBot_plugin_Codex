FROM ubuntu:latest

# 安装所需的软件包
RUN apt-get update && apt-get install -y openjdk-17-jdk build-essential python3 && apt-get clean

# 将main.py移入容器的/目录下
COPY main.py /main.py

# 设置工作目录
WORKDIR /
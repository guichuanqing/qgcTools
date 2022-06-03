#!/bin/bash

# 在 master 节点和 worker 节点都要执行

# 安装 docker
# 参考文档如下
# https://docs.docker.com/install/linux/docker-ce/centos/
# https://docs.docker.com/install/linux/linux-postinstall/

# 查看系统内核
uname -r

# 查看当前系统
cat /etc/os-release

# 卸载旧版本
yum remove -y docker \
docker-client \
docker-client-latest \
docker-ce-cli \
docker-common \
docker-latest \
docker-latest-logrotate \
docker-logrotate \
docker-selinux \
docker-engine-selinux \
docker-engine

# 安装基础依赖
yum -y install gcc
yum -y install gcc-c

# 设置 yum repository
yum install -y yum-utils \
device-mapper-persistent-data \
lvm2
yum-config-manager --add-repo http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo

# 安装并启动 docker
yum install -y docker-ce-20.10.14 docker-ce-cli-20.10.14 containerd.io
systemctl enable docker
systemctl start docker

# 关闭 防火墙
systemctl stop firewalld
systemctl disable firewalld

modprobe ip_vs
service docker restart

# 重启 docker
systemctl restart docker

docker run hello-world
docker version

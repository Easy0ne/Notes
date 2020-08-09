

## 计算命令执行时间
根据[time统计命令执行的时间](https://www.cnblogs.com/liuzhipenglove/p/7058726.html)实践：
time docker pull mysql将结果输出到标准输出(即屏幕)；
time docker pull mysql >> pullingtime.log并不能将time的输出定向到文件。
{ time docker pull mysql; } >>pullingtime.log可以实现(注意大括号后的空格)，并且只将time的输出定向到log文件中。

```bash
echo 'docker pull mysql' >> pullingtime.log
time docker pull mysql; >>pullingtime.log
```

## 开启docker的远程控制
首先需理解：
	- docker是由docker daemon监听docker client的请求，```service docker start```启动的是docker daemon；  
	- 了解Linux启动服务的两种方式service和systemctl；
	- docker可以使用dockerd手动启动、可以通过service启动、也可以通过systemd启动，这三者从后往前是包含关系(将前者的操作包含在本操作中)。
参考[docker docs: Optional post-installation steps](https://docs.docker.com/engine/install/linux-postinstall/#control-where-the-docker-daemon-listens-for-connections)，自定义docker daemon的配置有三种方式：
- 配置文件
	- 使用systemd 的Linux(如RedHat、CentOS、Ubuntu、SLES)可以通过docker.service来配置；
	- 其他版本Linux通过/etc/docker/daemon.json来配置，初次使用需要创建；(注意HTTP代理不能通过daemon.json来配置，需要在docker.service中配置)
- 使用dockerd启动时用参数的形式配置。
**以上三种配置方式中只能选择其中一种，否则会引起冲突而导致docker启动失败。**

开启远程控制需要让daemon监听连接，使用daemon.json配置，在文件中添加：
```
{
	"hosts": ["unix:///var/run/docker.sock", "tcp://0.0.0.0:2375"]
}
```
其中，docker.sock只能本地通过socket通信，0.0.0.0允许任何主机通信；
配置完成后重启docker，使用```netstat -lntp | grep dockerd```查看监听情况，使用docker info可以查看镜像源配置情况。  
在另一台装有Docker的主机上执行```docker -H 192.168.1.2:2375 image ls```便可实现远程控制。  

###其他
[安全的Docker daemon远程连接](https://www.cnblogs.com/wangmo/p/12938859.html)
Docker的其他配置参数见[docker docs: daemon configuration](https://docs.docker.com/engine/reference/commandline/dockerd/#daemon-configuration-file)，
常用的有docker-data、registry-mirrors等。
[Docker容器常用命令汇总](https://www.cnblogs.com/chenli90/p/10686108.html)

#@# [Docker查看镜像信息](https://www.cnblogs.com/quanxiaoha/p/10520049.html)
列出本机所有镜像:```docker images```。  
查看某一镜像的层信息：```docker history (ImageID|Repository:tag)```

### Linux下的目录
docker-data默认在/var/lib/docker下，可通过daemon.json修改。
Linux的/var/目录下是常变的文件，如日志、数据库以及docker的docker-data等数据文件；而/etc/下通常是配置文件。




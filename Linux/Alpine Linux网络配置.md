Alpine Linux配置网络

> 初次尝试可以使用Docker的小型Linux，看了大部分Linux网络配置的文章都是修改/etc/sysconfig/network-scripts/ifcfg-eth0文件的，但Alpine Linux没有这样的配置方式，搜了下"Alpine Linux network configure"，找到了[alpine wiki的网络配置部分](https://wiki.alpinelinux.org/wiki/Configure_Networking)，根据自己的需求配置了一遍，在此记录下。

##配置本机hostname  

```bash
echo 'slave1' > /etc/hostname
hostname -F /etc/hostname #立即生效
```

##配置hosts  
修改/etc/hosts文件：
```
192.168.1.150   shortname.domain.com
```

##配置Loopback  
添加文件 /etc/network/interfaces:
```
auto lo
iface lo inet loopback
```
即可设置IPv4的loopback地址127.0.0.1

##配置Ethernet    
以eth0为例：  

1. /etc/network/interfaces文件中，在所有eth0的配置项之前添加：  
```
auto eth0
```

2. Ipv4静态地址配置    
在/etc/network/interfaces文件的```auto eth0```之后添加：  
```
iface eth0 inet static
	address 192.168.1.150
	netmask 255.255.255.0
	gateway 192.168.1.1
```

##配置DNS  
修改/etc/resolv.conf文件：
```
nameserver 114.114.114.114
nameserver 114.114.115.115
```

## 关闭ipv6
有的域名解析会优先使用ipv6，由于未手动配置ipv6，可能会出问题。
修改/etc/modprobe.d/aliases.conf文件：
将```#alias net-pf-10 off```行解注释。
重启系统。  

---
ip和gateway也可以像其他Linux一样通过命令的方式临时配置：  

```
ifconfig eht0 192.168.1.150 netmask 255.255.255.0 up
route add default gw 192.168.1.1
```

---

	
---
VirtualBox中Alpine Linux + Docker安装记录
> 参照[Alpine Install: from a disc to a virtualbox machine single only](https://wiki.alpinelinux.org/wiki/Alpine_Install:_from_a_disc_to_a_virtualbox_machine_single_only)安装alpine会遇到一些问题，主要是网络配置和apk仓库引起的。
所以在此整理了下自己的安装过程。    

####1. “硬件”配置
在Preparing the virtual machine to install完成后，Virtualbox准备好了“硬件”，先不要Start，在Start之前需要先设置好网络，以保证在安装alpine时可以联网。  
具体操作：  
点击网络->网卡1->连接方式选择桥接网卡，其他默认。  
这种方式最容易配置网络的连接，可以在Alpine安装完成后再考虑其他连接方式，不同连接方式的区别见[virtualbox里的linux怎么配置网络连接](https://zhidao.baidu.com/question/1694543161515450868.html)。

####2. 启动并配置网络和apk仓库
设置中网络和存储设置好后(网络选择桥接网卡，存储中IDE有光驱iso，SATA有vdi虚拟硬盘)，然后Start。  
启动后，修改alpine的网络连接和apk仓库使得可以ping通仓库域名。  

#####2.1 网络连接  
ip和网关：  
```
ifconfig eht0 192.168.1.150 netmask 255.255.255.0 up
route add default gw 192.168.1.1
```
DNS：
```vi /etc/resolv.conf：  ```
```
nameserver 114.114.114.114
nameserver 114.114.115.115
```
关闭ipv6:
```vi /etc/modprobe.d/aliases.conf```
```alias net-pf-10 off```  

测试： ```ping https://mirrors.ustc.edu.cn/alpine/latest-stable/main  ```

> 也可以使用```dhclinet```命令通过DHCP获取ip、网关和DNS。  

#####2.2 apk仓库  
编辑/etc/apk/repositories文件 更改源：  
```
https://mirrors.ustc.edu.cn/alpine/latest-stable/main
https://mirrors.ustc.edu.cn/alpine/latest-stable/community
```
然后执行```apk update```更新apk indexs。

####3. 安装Alpine  
以上准备工作完成后，运行setup-alpine开始安装。  
	- 键盘布局选择cn，cn之后再cn
	- hostname随意
	- 网络相关配置默认都为第2步中所配
	- root密码修改为123456会提示too weak，但可以使用
	- Timezone选择Hongkong
	- 镜像已配
	- SSH server使用默认的openssh
	- NTP使用默认的Chrony，轻小
	- disk选择virtualbox分配的vdi，名为sda
	- How to use it? 选择sys，因为要安装alpine到这个vdi中
	- 提醒会擦除vdi，确认是你要安装的那个后输入y回车就开始执行安装了。

####4. 关机、从虚拟硬盘启动  
安装完成后，执行```poweroff```关机，然后修改这个虚拟机的启动：  
选择该虚拟机->设置->存储->选择盘片右击删除；系统->取消勾选光驱。    
再次启动后以root登录就需要输入密码了。

####5. 安装docker
参照[alpine linux 环境中安装 docker](http://www.imooc.com/article/287437)安装docker，测试网络连接没问题后，执行```apk add docker```安装docker，如果提示missing错误，检查/etc/apk/repositories文件，不过我用的是中科大的两个镜像仓库，目前只有社区仓库(通常以community结尾)中才有docker。

####6. 配置docker
/etc/docker/daemon.json的配置在各种Linux版本之间通用，一些Linux没有systemd。  
在其中添加```"registry-mirrors": ["https://registry.docker-cn.com", "https://docker.mirrors.ustc.edu.cn", "http://hub-mirror.c.163.com"]```

####7. 启动docker
执行```service docker start```启动Dockers daemon。
执行```docker run hello-world```测试。


---
###其他参考

[alpine Linux中安装docker](http://www.imooc.com/article/287437)  
[alpine 包管理工具apk](https://www.cnblogs.com/kuku0223/p/8421964.html)
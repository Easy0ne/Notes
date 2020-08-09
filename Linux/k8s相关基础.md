# k8s基础

## etcd
etcd是一个键值存储仓库，用于配置共享和服务发现。
参考[ETCD简介与使用](https://blog.csdn.net/bbwangj/article/details/82584988)，是个类似于Zookeeper的项目。

## 架构


## 安装组件
kubeadm + kubelet + kubectl
### kubeadm
负责安装k8s,在kubeadm之前，所有组件需要逐个手动安装
### kubelet
负责启动container
### kubectl
命令行，类似于docker command

## 其他
### Google 为服务架构解决方案
Golang + gRPC + Istio

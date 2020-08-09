# 进程学习小结  

##[进程的创建和终止](http://c.biancheng.net/view/1207.html)
### 进程树
- ![Linux进程树](http://c.biancheng.net/uploads/allimg/181102/2-1Q1021100135W.gif)  
init为根进程，login、kthreadd、sshd等为其子进程
### 进程的创建
- ![通过系统调用fork()创建进程](http://c.biancheng.net/uploads/allimg/181102/2-1Q102110425511.gif) 
父子进程都执行fork()之后的代码，根据fork()返回的pid>0?来区分父子进程，从而执行不同程序。  
- 子进程的资源可以从操作系统处获得，也可以只从父进程处获得。限制子进程只能使用父进程的资源可以防止创建过多的进程而导致系统超载。
### 进程的终止
进程执行完后会显式或隐式调用exit()，由操作系统释放内存、文件和I/O缓冲区等资源，但进程表中的条目信息还在，直到它的父进程调用wait()。
- 僵尸进程：当进程终止时，其父进程尚未调用wait()，这个进程就被称为僵尸进程。所有进程都会过渡到这种状态，正常情况下僵尸状态只是短暂存在。一旦父进程调用了 wait()，僵尸进程的进程标识符和它在进程表中的条目就会释放。  
- 孤儿进程：如果某个进程的父进程没有调用 wait() 就终止退出了，则这个进程就成为孤儿进程。linux和unix的处理办法是将init进程作为孤儿进程的父进程，init进程定期wait()，以便收集任何孤儿进程的退出状态，并释放孤儿进程标识符和进程表条目。  
- 有的系统不允许子进程在父进程已终止的情况下存在，通常会使用级联终止，即，如果一个进程终止（正常或不正常），那么它的所有子进程也应终止。

## [进程间通信(IPC)](https://blog.csdn.net/zhaohong_bo/article/details/89552188)  
### 管道
半双工，本质是一个内核缓冲区
- 无名管道pipe，只能用于父子进程间通信，因为管道没有全局名字(跨进程的)，所以进程只能访问自己或祖先通过pipe()系统调用创建的管道。
- 有名管道fifo，有自己的名字，并且对应于一个磁盘索引节点node，有了这个文件名，任何进程有相应的权限都可以访问，Linux中通过mknod()或makefifo()来创建。当一个命名管道不再被任何进程打开时，它并不会消失，如果要删除应该用删除普通文件的方法来删除(实际上删除的是磁盘上对应的节点信息)。
###消息队列
消息队列是一系列保存在内核中消息的列表，一个消息队列由一个标识符来标识；
消息队列中的消息具有特定的格式和特定的优先级；
消息队列独立于发送和接收程序，当进程终止时，消息队列机器内容并不会被删除；
消息队列克服了信号传递信息少、管道只能承载无格式字节流以及缓冲区大小受限等缺点。
### 共享内存
由一个进程创建，允许多个进程将这块共享的存储区映射至自身的地址空间，是最快的IPC方式(管道和消息队列还需要在内核和用户空间切换)；因为多个进程可以同时操作，所以需要实现同步，通常与其他IPC机制(信号量)配合。

### 信号量
是一个计数器，用于实现进程间的同步和互斥，而不是存储数据。
基于操作系统的PV操作，程序对信号量的操作都是原子操作。
### 套接字


### 挂起与阻塞的区别  

- 挂起一般是主动的(需要调用挂起函数来操作)，会将进程暂时从内存调到外存，不同于阻塞状态等待事件或资源(你不知道他什么时候被阻塞，也就不能确切地知道他什么时候恢复阻塞)，挂起后的恢复需要主动完成；而且，挂起队列在OS里可以看成只有一个，而阻塞队列是不同的事件/资源(如信号量)有自己的队列。  
- 任务调度是操作系统来实现的，任务调度时，直接忽略挂起状态的任务，如果不主动恢复，则此任务就一直不会就绪。而阻塞的任务等到需要的资源或事件后，就可以转为就绪状态。

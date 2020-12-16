[TOC] 

# Mac 常用命令记录

## top
top命令运行包含两种模式：logging mode 和 interactive(non-logging) mode.  
### logging mode
像通常只用看一眼当前内存等占用多少、还剩多少，使用logging mode即可：
` top -l 1 | head -n 10 ｜ grep PhysMem`。
其中-l表示使用logging mode，1表示取1个samples。
可以在~/.zshrc中添加自己的alias：
` alias topcm="top -l 1 | head -n 10 | grep 'CPU\|PhysMem'" `。

此外，查看内存使用情况还可以使用vm_stat命令，
[github-macfree](https://github.com/smilejay/python/blob/master/py2014/mac_free.py)给了一个python脚本对vm_stat的结果进行处理，只统计macOS主要分类的内存使用(wired、active、inactive和free)情况，
具体含义可以看[MAC上命令行查看系统内存使用量](http://smilejay.com/2014/06/mac-memory-usage-command-line/)。  
将py文件放在`~/bin`下(不必要但建议)，并`python -O -m py_compile mac_free.py`将其编译成pyo，然后`alias macfree="python ~/bin/mac_free.pyo"`  

### interactive mode
top默认使用interactive mode，不必要的情况下可以使用`-s`(delay-secs)延长更新时隙:` top -s 10 `, 每10秒刷新一次，当然也可以按回车手动刷新。

进入交互后：

- 按下`o`，输入mem，可根据memory使用进行排序（order）；
- 按下`O`，输入cpu，则将cpu占用率作为第二主键进行排序；
- 按下`U`，输入用户名/uid，则只展示属于该用户的进程。
- 按下`?`，可查看其他交互方式。

## 后台运行
> 参考[后台执行命令](https://blog.csdn.net/liuxiao723846/article/details/47754479)  

像find、数据量较大的排序以及一些shell脚本通常执行时间较长，适合放在后台运行。

1. 运行:

- `cmd & `可以将命令放到后台运行，同时会显示进程号，但输出还是会输出到当前终端stdout，所以通常是将输出重定向到某个文件中，例如：
` cmd > cmd_print.out 2>&1 & `。具体含义参考[Linux&、 2>&1是什么](https://blog.csdn.net/lovewebeye/article/details/82934049)
- 但只使用`&`的话，在当前控制台关掉时也会被停止（是当前console的子进程？），所以，通常配合`nohup`(no hang up)命令使用:
` nohup cmd > cmd_print.out 2>&1 &`。  
- ctrl+z 可以将当前正在运行的命令suspend到后台，并且暂停运行。 ctrl+c是终止运行。

2. 查看:

- jobs:  
`jobs -l`可显示所有任务的PID
- bg:  
`bg`将一个在后台暂停的命令，变成在后台继续执行。如果后台中有多个命令，可以用bg %jobnumber将选中的命令调出。
- fg:  
`fg`将后台中的命令调至前台继续运行。如果后台中有多个命令，可以用fg %jobnumber将选中的命令调出。


3. 另外再说下windows的后台运行：  
`start /b cmd`可让cmd在后台运行，
例如，`start /b python test.py`, 然后`tasklist`查看进程。  


## 查找文件
主要是不想看到Permission denied及其他错误信息：
` find / -name 'Caskroom' -print 2>/dev/null `  
或者过滤掉不想看到的：
`find / -name 'Caskroom' -print 2>&1 | fgrep -v 'Permission denied'`


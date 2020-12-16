# 新 Mac - M1 MBA 安装软件记录
## 安装homebrew
> 参考[苹果M1 Mac上怎样使用Homebrew？](https://zhuanlan.zhihu.com/p/336132667) 

1. 安装  
目前arm版homebrew必须安装在/opt/homebrew下:  

```
cd /opt/ 
mkdir homebrew
sudo chown -R $(whoami) /opt/homebrew # 当前用户接管该目录
curl -L https://github.com/Homebrew/brew/tarball/master | tar xz --strip 1 -C homebrew
```

2. 配置  
由于/opt/homebrew/bin/不在$PATH中，需要手动添加。  
首次配置需要创建文件`~/.zshrc`文件，然后添加。  
也可以使用alias以便区分x86 brew和arm brew。
```
touch ~/.zshrc 
cat >> ~/.zshrc
alias abrew=/opt/homebrew/bin/brew
# export PATH=$PATH:/opt/homebrew/bin:.
```

## 安装git
1. 安装Command Line Tools
执行` brew search git ` 会提示需要安装开发者命令行工具（CLT），但点击同意后安装的是整套xcode，需要一个多小时，不搞ios开发自然是不装。  
网上的` xcode-select --install ` [方法](https://www.zhihu.com/question/37165801/answer/133590569)也不能只安装CLT，所以到 [More Downloads for Apple Developers](https://developer.apple.com/download/more/)中下载macOS对应版本的CLT安装包（可以参考app store中xcode的历史版本记录）。

2. 安装git
其实安装完CLT就已经包含git了，如果不是想要的版本可以再安装:  
` brew install git `
> 我之后安装python3.8发现这个CLT也包含了…。可以到`/Library/Developer/CommandLineTools/usr/bin`下看已经包含的工具.


## 一些发现
1. Mac的文件系统APFS分为了一个数据卷（ Macintosh HD Data）和一个系统卷（ Macintosh HD），系统卷是挂载在数据卷的`/System/Volumes/Data`目录下，APFS使用firmlink使得开发者可以两个卷之间互相访问。详见[当 Mac 升级到 Catalina 时，苹果在硬盘里施了点魔法](https://sspai.com/post/57052)。
2. python在import的时候是先找有没有pyc/pyo，没有的话再读入py文件。详见[python文件的编译](https://www.cnblogs.com/lijingchn/p/5355018.html)

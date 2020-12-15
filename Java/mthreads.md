


### 操作系统的线程与JVM线程
[Java的线程管理器能保证每个线程都有执行的机会么](https://www.zhihu.com/question/27491155/answer/36847691)

### wait/yield/sleep/join都做了什么
先理解线程的状态：创建、就绪、运行、阻塞、死亡。
其中，进入阻塞态主要有三种方式：
- 等待阻塞：线程调用wait()方法，释放所有资源，之后只能等别的线程调用notify/notifyAll方法来唤醒；
- 同步阻塞：获取同步锁失败
- 其他阻塞：线程执行Thread.sleep()方法或join()方法，或者发出I/O请求，JVM会将线程置为阻塞态，直到sleep时间结束、join等待的线程终止或者I/O处理完毕才重新就绪。
理解状态转换后，再看这几个方法：
- Object.wait()：线程释放CPU资源、锁，然后进入阻塞态，直到被其他线程唤醒才进入就绪态。wait和notify/notifyAll要在synchronized代码块中调用。
- Thread.sleep()：当前线程释放CPU资源但不释放锁资源，进入阻塞态，直到时间结束。生产环境几乎不会使用。
- yield()：线程释放CPU资源、不进入阻塞态而直接进入就绪态，主要用来让更高优先级的线程先执行。
- thread1.join()：等待thread1线程运行结束。
TOC

### ==、equals()以及hashcode()
ref: [==、equals()、hashcode()](https://www.cnblogs.com/kexianting/p/8508207.html)
1. ```==```比较的是对象地址(引用)，看是否为同一对象  
Integer与int会自动拆箱、Integer和String的缓存(Integer默认-128~127，String缓存用过的、但new的就是new的)
2. ```equals()```比较的是内容  
但Object默认是使用==实现，Java内置类都已重写，自定义的类也需要重写
3. ```hashcode```应跟随```equals()```的重写   
equals重写后hashcode也应该重写(Java规范，但不是语法级的)，因为两个对象equals，则他们的hashcode也应该相同。  
Object默认的hashcode方法是native的，是根据对象地址进行计算的。自定义类重写hashcode方法见[自定义类如何重写hashcode()方法](https://www.cnblogs.com/stitchZsx/p/9558843.html)


### 加号+
1. Java中“+”有两个作用：加法和字符串拼接。  
1.1 当“+”两边的操作数至少有一个是字符串时，“+”的作用是字符串拼接，底层实现是调用new StringBuilder().append()方法，当有大量的“+”时会生成很多StringBuilder对象  
1.2 当“+”两边都是数值型操作数时，“+”的作用是加法计算
1.3 注意char不是字符串，char在内存中是以整数形式存在的。

2. 输出集合元素时，除了字符串拼接的方法(+、StringBuilder.append)，还可以考虑stream终端操作。
String的+是调用了new StringBuilder().append()方法


### String、StringBuilder、StringBuffer
1. String
String的value[]数组是final的，不可修改，对string进行拼接/修改时会创建新的String对象。

2. StringBuffer
StringBuffer正是为了解决修改String产生过多中间对象的问题(```@Since JDK1.0```)，提供append、replace、insert、delete等方法，但它是线程安全的，开销较大；

3. StringBuilder
StringBuilder(```@Since JDK1.5```)是为了解决StringBuffer开销大的问题，去掉了StringBuffer的synchronized，，更高效；  
StringBuffer 和 StringBuilder二者都继承自AbstractStringBuilder ，底层都是利用可修改的char数组。

4. 用哪一个
少量字符串操作还是用String，易读；  
需要大量拼接/修改操作时，根据是否需要线程安全来选择StringBuffer和StringBuilder。  
使用StringBuffer 和 StringBuilder时注意能预知大小就在new的时候设置好capacity，避免扩容开销(二者默认capacity为16，扩容时会用Arrays.copyOf()丢弃原有数组然后创建新的数组)。


### 从JVM的字符串常量池理解String.intern()
####ref1: [从字符串到常量池，一文看懂String类](https://blog.csdn.net/qq_41907991/article/details/106799400)   
class文件的结构  
class常量池中存的是字面量和符号引用，也就是说他们存的并不是对象的实例，经过解析（resolve）之后，才会把符号引用替换为直接引用  
不同版本的JVM内存模型  
字符串常量池中实际存放的是字符串的引用，而不是字符串实例  
String s = new String("1")是怎么产生两个对象的  
JDK1.6和JDK1.7对intern方法的实际操作区别(主要是1.7将驻留字符串实例都存放在堆中，可以直接让一个常量池引用指向驻留字符串，而不用将堆中的字符串对象拷贝到没有该字符串的永久代中)   
String s1 = new String("1") + new String("1")实际还调用了StringBuilder.append()方法  
JDK1.6的永久代、1.7/1.8的元空间都是对方法区的不同实现  

####ref2: [美团-深入解析String.intern()](https://tech.meituan.com/2014/03/06/in-depth-understanding-string-intern.html)   
- Java为了提高运行速度及节省内存，为8种基本类型和String都提供了常量池；
- 基本类型的常量池是系统协调的，字符串常量池有两种使用方法：双引号引用，String.intern()
- JDK1.7之前，字符串常量池位于Perm区，而Perm区默认只有4M；由于字符串常量池太占Perm区空间，1.7将字符串常量池移到堆中。
- 1.7中调用intern()时，不再复制字符串到Perm区的字符串常量池中(然后StringTable中一个item指向这个驻留字符串)，而是让堆中字符串常量池的StringTable指向这个对象，使其成为驻留字符串；
- String pool是通过维护StringTable指向字符串来维护字符串常量池的，StringTable的实现与HashMap相似，只是不能扩容，默认StringTable的数组容量只有1009，如果使用intern往StringTable中放入了过多的指向驻留字符串的引用，就会产生Hash冲突，链表增长，导致继续调用intern()时性能大幅下降。



### stream操作
[JDK8 Stream 数据流效率分析](https://blog.csdn.net/Al_assad/article/details/82356606)	  
1.怎么用
- 数据源：Collection、I/O流
- 中间操作：map()、filter()、distinct()、sorted()、limit()、mapToInt()、boxed()……
- 终端操作：收集为Collection、收集为Array、收集为String、count统计元素数量、max统计最大值、min统计最小值……

2.特点
- 只遍历一次，流水线操作
- 内部迭代，而Collector的Iterator是一种外部迭代

3.什么时候用
- 在小规模的集合(<10000)中，stream的效率其实不如iterator，但遍历开销基本上都小于1毫秒，即使是成倍的差距也可忽略不计；
而stream的写法要比iterator高效且易读，尤其是要进行多种操作时。
- 在超大规模的集合中(>1000w)，stream的遍历效率要好于iterator，但也不会好太多，parallelStream会好很多(前提时能用到多核)。




## 推荐阅读
[美团技术团队](https://tech.meituan.com/tags/java.html)
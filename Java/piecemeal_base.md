[TOC] 
---

### 运算符优先级
[java运算符优先级记忆口诀](https://www.cnblogs.com/gavin-yao/p/10595835.html):  
单目乘除为(位)关系，逻辑三目后(填词，无意义)赋值。  
强制类型转换优先级是高于乘除但低于单目的：
```java
int a = (int) Math.random()*10
// a始终为0
```
实际开发中不用刻意去记，小括号写着方便也易读懂。

### ==、equals()以及hashcode()
ref: [==、equals()、hashcode()](https://www.cnblogs.com/kexianting/p/8508207.html)
1. ```==```比较的是对象地址(引用)，看是否为同一对象  
Integer与int会自动拆箱、Integer和String的缓存(Integer默认-128~127，String缓存用过的、但new的就是new的)
2. ```equals()```比较的是内容  
但Object默认是使用==实现，Java内置类都已重写，自定义的类也需要重写
3. ```hashcode```应跟随```equals()```的重写   
equals重写后hashcode也应该重写(Java规范，但不是语法级的)，因为两个对象equals，则他们的hashcode也应该相同。  
Object默认的hashcode方法是native的，是根据对象地址进行计算的。自定义类重写hashcode方法见[自定义类如何重写hashcode()方法](https://www.cnblogs.com/stitchZsx/p/9558843.html)


### 加号"+"
1. Java中“+”有两个作用：加法和字符串拼接。  
1.1 当“+”两边的操作数至少有一个是字符串时，“+”的作用是字符串拼接，底层实现是调用new StringBuilder().append()方法，当有大量的“+”时会生成很多StringBuilder对象    
1.2 当“+”两边都是数值型操作数时，“+”的作用是加法计算  
1.3 注意char不是字符串，char在内存中是以整数形式存在的。 

2. 输出集合元素时，除了字符串拼接的方法(+、StringBuilder.append)，还可以考虑stream终端操作。
String的+是调用了new StringBuilder().append()方法


### Java中父子类的构造函数、静态变量、代码块的执行顺序

这种题做了两三次了，每次都记不住代码块应该什么时候执行，还是先学习下代码块的概念和作用。  
1. [代码块](https://www.jianshu.com/p/49e45af288ea)
Java中代码块指的是用 {} 包围的代码集合，分为4种：普通代码块，静态代码块，同步代码块，构造代码块
- 普通代码块，这个普通代码块的概念容易被误解，它不是这类题中所说的代码块，而是我们在方法中常见的，包括方法、循环、判断等语句中出现的代码块；
- 静态代码块也好理解，类中static修饰的代码块，在加载类的时候会执行，一般用于静态变量的初始化，有多个静态代码块的话就按照出现顺序先后执行；
- 同步代码块也好理解，可以简单地认为就是synchronized修饰的普通代码块；
- 构造代码块，这个就是这类题中常说的代码块——在类中定义且没有加任何修饰的代码块，它的作用其实就是初始化实例变量，可能会想到这不是构造函数的活吗，是的，不过它是把多个构造函数中的公共代码提取出来了~~它的执行依赖于构造函数，编译器在编译的时候会把构造块代码插入到构造函数的最前面。

2. 执行顺序实例
```java
public class Test {
    public static void main(String[] args) {
        new Square();
        System.out.println("--------Next---------");
        new Circle();
    }
}

 class Shape {
    public Shape() { System.out.println("Shape Constructor Func.");}
    static { System.out.println("Shape static code1.");}
    static { System.out.println("Shape static code2.");}
    { System.out.println("Shape constructor code block.");}
}

class Square extends Shape {
    public Square() { System.out.println("Square Constructor.");}
    static { System.out.println("Square static code.");}
    { System.out.println("Square normal code.");}
}

class Circle extends Shape {
    public Circle() { System.out.println("Circle Constructor.");}
    static { System.out.println("Circle static code.");}
    { System.out.println("Circle normal code.");}

}
```

执行结果：
```shell
Shape static code block 1.
Shape static code block 2.
Square static code block.
Shape constructor code block.
Shape Constructor Func.
Square constructor code block.
Square Constructor Func.
--------Next--------
Circle static code block.
Shape constructor code block.
Shape Constructor Func.
Circle normal code block.
Circle Constructor Func.
```

分析：   
2.1 首先可以确定的是会先加载类执行static代码块，但父子类会先加载哪一个呢？从结果可以看出是先加载父类再加载子类，但我在想，反正父类的类变量也不会被子类继承，先执行子类静态代码块好像也不会出错？这块我还没搞清楚，可能跟类信息的描述有关？想起方法区会加载类信息，这里需要先加载父类的类信息？如果是这样的话，那就会顺着继承链向上找到祖先类？这里还没搞清楚，先挖个坑。这里记住先加载父类就好了。  
第二个点就是，Circle类的加载是在```new Circle()```的时候执行的，不是像我之前想的那样先把所有的类都加载上。  
总之，类加载这里我还是没搞清楚，还请大佬赐教指正。

2.2
上面说构造代码块会被编译器插入到构造函数的最前面，但这个最前面也是在super()后面的。

2.3 总结下顺序就是父类static代码块 -> 子类static代码块 -> 父类构造代码块 -> 父类构造函数 -> 子类构造代码块 -> 子类构造函数


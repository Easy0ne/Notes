[TOC] 
---


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


### stream操作
[JDK8 Stream 数据流效率分析](https://blog.csdn.net/Al_assad/article/details/82356606) 
1. 怎么用
- 数据源：Collection、I/O流
- 中间操作：map()、filter()、distinct()、sorted()、limit()、mapToInt()、boxed()……
- 终端操作：收集为Collection、收集为Array、收集为String、count统计元素数量、max统计最大值、min统计最小值……
```java
List<Integer> itgList = new ArrayList<Integer>();
Random random = new Random();
        for (int i = 0; i < 10; i++) itgList.add(random.nextInt());
List<Integer> streamList = itgList.stream()
                .mapToInt(x -> x)
                .map(x -> x+1)
                .filter(x -> x>200)
                .sorted()
                .boxed()
                .collect(Collectors.toCollection(ArrayList::new));
				
List<String> strList = new ArrayList<String>();
        for (int i = 0; i < 10; i++)  strList.add("str");
String strResult = strList.stream()
                .collect(Collectors.joining(","));
```

2. 特点
- 只遍历一次，流水线操作
- 内部迭代，而Collector的Iterator是一种外部迭代

3. 什么时候用
- 在小规模的集合(<10000)中，stream的效率其实不如iterator，但遍历开销基本上都小于1毫秒，即使是成倍的差距也可忽略不计；
而stream的写法要比iterator高效且易读，尤其是要进行多种操作时。
- 在超大规模的集合中(>1000w)，stream的遍历效率要好于iterator，但也不会好太多，parallelStream会好很多(前提时能用到多核)。
- 使用建议：stream中含有装箱类型时，在进行中间操作前，最好手动转成对应的数值流，减少频繁的拆箱装箱而引起的性能损失，最后再boxed()装回去。

### Comparable接口和Comparator接口
1. Comparable
一个类(比如基本类型的封装类以及String类等，是的，连Boolean也实现了)实现了Comparable接口(实现compareTo()方法)，则该类自带比较器。  
在```Arrays.sort(T[], Comparator c)```、```Collections.sort(List l ist)```方法中，隐含传递着Comparator参数为null，在排序比较时直接调用该类对象.compareTo(T another)方法。  
```compareTo(T another)``` 返回正数则表示当前对象大于another。

2. Comparator
Comparator就是个外部比较器了，主要是提供给那些没有实现Comparable接口的类。  
在```Arrays.sort(T[], Comparator c)```、```Collections.sort(List list, Comparator c)```方法中，需要自定义Comparator接口并实现其```compare(T o1, T o2)```方法，在排序比较时会调用该方法。  
```compare(T o1, T o2)```返回整数则表示o1大于o2。  
```java
int[] arr = new int[10];
Collections.sort(Arrays.stream(arr).boxed().collect(Collectors.toList()),
                    new Comparator<Integer>() {
                        @Override
                        public int compare(Integer o1, Integer o2) {
                            return 0;
                        }
                    }
            );
			
// Arrays.stream(arr).boxed().collect(Collectors.toList()).sort((x1, x2) -> x1 - x2);
```
3. Collections、Arrays
Collections排序有两个方法，```Collections.sort(List list)```和```Collections.sort(List list, Comparator c)```，看到这个sort方法就会想起```Arrays.sort()```方法，再考虑到ArrayList/Vector、HashMap、HashSet(内部维护一个HashMap)内部都是维护一个数组，就会想到是不是也可以用Arrays.sort()方法。  
继续看```Collections.sort```的实现，其实际上是调用```list.sort(c)```方法，而list.sort又是调用```Arrays.sort(list.toArray())```方法，这样连LinkedList也转为数组来调用```Arrays.sort()```。【这么看来，其实List对象的排序可以直接用```list.sort(Comparator c)```。】  
```java
// Collections.java
public static <T> void sort(List<T> list, Comparator<? super T> c) {
        list.sort(c);
    }

//List.java
default void sort(Comparator<? super E> c) {
        Object[] a = this.toArray();
        Arrays.sort(a, (Comparator) c);
        ListIterator<E> i = this.listIterator();
        for (Object e : a) {
            i.next();
            i.set((E) e);
        }
    }
``` 
那HashMap呢？   


4. [HashMap的排序](https://zhuanlan.zhihu.com/p/80455770)
主要是两种思路：
- 转为TreeMap
- HashMap本身是一个集合，可以利用集合的排序：Collections.sort/Arrays.sort、Stream API

4.1 转为TreeMap
```java
	TreeMap<String, Integer> treeMap = new TreeMap<>(unsortedMap);
    System.out.println(treeMap);

```

4.2 Collections.sort
```java
	List<HashMap.Entry<String, Integer>> listOfMap = new ArrayList<>(unsortedMap.entrySet());
	Collections.sort(listOfMap, (o1, o2) -> o1.getKey().compareTo(o2.getKey()));
	System.out.println(listOfMap);
```
这种方法比较灵活，可以根据key排序，也可以根据value排序；转List也可以只获取key(.keySet())，也可以只获取value(.values())，也可以都保存(.entrySet())。

4.3 Stream API
这里要知道的是，集合类包含两大系统，Collection接口和Map接口。
- Collection接口下有List接口、Set接口和Queue接口。
- Map接口就是Map系列，需要排序则实现SortedMap接口；但Map可以生成Collection。
而Collection接口有stream()方法，可以获得集合的stream，而Map接口没有。  
所以这里也是像Collections.sort那样，获取map的entrySet/keySet/values。
```java
List<String> sortedKeyList = unsortedMap.keySet().stream()
                .sorted(String::compareTo)
                .collect(Collectors.toList());
System.out.println(sortedKeyList)
```

### int[]、Integer[]、List<Integer>之间的转换
```java
public void testTransform() {
        /*
        关键在对Stream的使用上
        首先是将其接入到stream上
        数组通过Arrays.stream()
        集合(List和Set，Map得获取Set或List)直接通过.stream()

        然后是中间转的操作
        Integer到int使用mapToInt(x -> x)
        int到Integer使用boxed()

        最后是stream到终端
        导出为int[]使用.toArray();
        导出为Integer[]使用.toArray(Integer::new);
        导出为List使用.collect(Collectors.toList());
        导出为LinkedList/ArrayList使用.collect(Collectors.toCollect(ArrayList::new));
         */

        Random random = new Random();

        // IntStream to int[]
        int[] ints = random.ints(5, 0, 10)
                .toArray();

        // IntStream to Integer[]
        Integer[] integers = random.ints(5, 0, 10)
                .boxed().toArray(Integer[]::new);

        // IntStream to List<Integer>
        List<Integer> integerList = random.ints(5, 0,10)
                .boxed().collect(Collectors.toList());

        // List<Integer> to Integer[]
        Integer[] integers1 = integerList.stream()
                .toArray(Integer[]::new);

        // List<Integer> to int[]
        int[] ints1 = integerList.stream()
                .mapToInt(x -> x)
                .toArray();

        // int[] to List<Integer>
        List<Integer> integerList1 = Arrays.stream(ints)
                .boxed()
                .collect(Collectors.toList());

        // int[] to Integer[]
        Integer[] integers2 = Arrays.stream(ints)
                .boxed()
                .toArray(Integer[]::new);

        // Integer[] to List<Integer>
        List<Integer> integerList2 = Arrays.stream(integers)
                .collect(Collectors.toList());

        // Integer[] to int[]
        int[] ints2 = Arrays.stream(integers)
                .mapToInt(x -> x)
                .toArray();


        /*
        -------------------------------------------------------------------
         */
        // String to Set<Character>
        String s = "12,23,34,45,55";
        Set<Character> characterSet = s.chars()
                .mapToObj(x -> (char) x)
                .collect(Collectors.toSet());

        LinkedHashSet<Character> characterLinkedHashSet = s.chars()
                .mapToObj(x -> (char) x)
                .collect(Collectors.toCollection(LinkedHashSet::new));

        System.out.println(characterLinkedHashSet);
    }
```

### Pattern和Matcher——字符匹配
参考[Java Pattern和Matcher字符匹配详解](https://blog.csdn.net/zengxiantao1994/article/details/77803960)  
1. Pattern  
经典的用法，配合Matcher对象：
```java
Pattern p =Pattern.compile("\\d+");
// Pattern的构造方法是私有的，通过静态的简单工厂方法compile创建Pattern对象，并且此对象是不可改变的，是线程安全的，可供过的Matcher使用。
Matcher m =p.matcher("23ab23");
boolean b = m.matches();
```
也可：
```java
boolean b =Pattern.matches("a*b", "aaaaab");
// 单次匹配可用它
```
示例：
```java
// 使用Pattern.compile方法编译一个正则表达式，创建一个匹配模式
Pattern pattern = Pattern.compile("\\?|\\*");

// split方法对字符串进行分割
// 123 123 456 456
String[]splitStrs = pattern.split("123?123*456*456");
for (int i = 0; i < splitStrs.length; i++) {
	System.out.print(splitStrs[i] + "  ");
}

// Pattern.matches用给定的模式对字符串进行一次匹配，（需要全匹配时才返回true）
System.out.println("Pattern.matches(\"\\\\d+\",\"2223\") is " + Pattern.matches("\\d+", "2223"));
System.out.println("Pattern.matches(\"\\\\d+\", \"2223aa\")is " + Pattern.matches("\\d+", "2223aa"));
```
2. Matcher  
2.1. Matcher类提供了三个匹配操作方法，三个方法均返回boolean类型，当匹配到时返回true，没匹配到则返回false。  
	- boolean matches()最常用方法：尝试对整个目标字符展开匹配检测，也就是只有整个目标字符串完全匹配时才返回真值。
	- boolean lookingAt()对前面的字符串进行匹配，只有匹配到的字符串在最前面才会返回true。
	- boolean find()：对字符串进行匹配，匹配到的字符串可以在任何位置。    
2.2. find()方法通常需要配合匹配器的状态来完成后续操作：
	- intstart()：返回当前匹配到的字符串在原目标字符串中的位置；
	- int end()：返回当前匹配的字符串的最后一个字符在原目标字符串中的索引位置；
	- String group()：返回匹配到的子字符串。
以上三个方法均有相应的重载方法: int start(int i)，int end(int i)，int group(int i)，Mathcer类还有一个groupCount()用于返回有多少组。  
2.3. 此外，Matcher类还有String replaceAll(Stringr eplacement)、String replaceFirst(Stringreplacement)等方法，String.replaceXXX()方法就是调用此方法的。  
3. 实例：
```java
Pattern p = Pattern.compile("([a-z\\|A-Z]+)(\\d+)(\\d+[a-z|A-Z]+)");
Matcher m = p.matcher("aA2323Aa");
m.find();
for (int i = 0; i <= m.groupCount(); i++) {
	System.out.println(String.format("group(%d) is %s,\t\t start(%d) is %d,\t\t end(%d) is %d",
			i, m.group(i), i, m.start(i), i, m.end(i)));
}
```

4. 其他：
[贪婪与非贪婪的使用](https://blog.csdn.net/qq_41455420/article/details/79810006)  


### List使用的一些注意事项
1. 遍历时删除  
	``` List<String> list = new ArrayList<>();```  
	``` for (String s: list) list.remove(s)``` 肯定是不行的，Java集合类都含有一个modCount属性，每次增删改都会modCount++，其内部迭代器的next()方法会先调用checkForComodification()方法判断modCount == expectedModCount(expectedModCount是Iterator的属性，modCount是集合对象的属性)。

2. Iterator.remove()  
	remove会调用list的remove()方法，但在调用后会令expectedModCount = modCount，从而在checkForComodification()时通过检查。
	```java
	 Iterator<String> iterator = list.iterator();
        while (iterator.hasNext()) {
            String s = iterator.next();
            if ("d".equals(s)) {
                iterator.remove();//使用迭代器的删除方法删除
            }
        }
	```
3. for i的外部迭代方式
	```java
        for (int i = 0; i < list.size(); i++) {
            System.out.println("list当前长度:" + list.size());
            if ("d".equals(list.get(i))) {
                // list.remove(i); 直接删除会让i后面的那个转移到i的位置，从而不经过下次if检查。
				// list.remove(i--);
            }
        }
	```
	或者直接倒叙遍历删除。


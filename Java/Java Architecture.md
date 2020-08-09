

## Dubbo + Zookeeper
### dubbo 
dubbo是一个远程调用的分布式框架，有点像web service的WSDL，它是通过dubbo协议(dubbo://xxx.xxx)进行点对点通讯，分为Provider端和Consumer端(也可以理解为服务端和客户端)，两端共用一个接口包，Provider端面向接口实现，Consumer端面向接口调用。  
Provider端实现后通过Provicer.xml的Spring配置暴露服务(dubbo:protocol 指定协议为dubbo)，Consumer端通过Consumer.xml(dubbo:reference 给出服务的dubbo地址)得到Contex。Consumer.xml的同一服务可以给出多个dubbo地址，并可以指定负载均衡策略。
### zookeeper
如上所说，当同一服务有新的provider时，consumer需要更新其配置文件才能调用新的provider服务。zookeeper正是在这种情况下担任了注册与发现中心的角色：  
1. provider都向zookeeper注册服务；
2. consumer向zookeeper订阅，获得可用的provider列表；
3. consumer从列表中根据软负载均衡算法选取一个provider进行调用；
4. provider和consumer在内存中累积调用次数和调用时间，定时将这些统计数据发送给monitor。
provider在Provicer.xml中配置dubbo:registry协议为zookeeper并给出zookeeper服务器地址；  
consumer在Consumer.xml中配置dubbo:registry协议为zookeeper，在dubbo:reference中无需指定url。  
具体配置及流程见[dubbo和zookeeper的关系](https://www.cnblogs.com/iisme/p/10620125.html)


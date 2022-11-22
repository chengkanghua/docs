# 操作etcd

#### [ETCD常用操作](http://49.7.203.222:2023/#/kubernetes-advanced/etcd?id=etcd常用操作)

官网： https://github.com/etcd-io/etcd

拷贝etcdctl命令行工具：

```bash
wget https://github.com/etcd-io/etcd/releases/download/v3.5.3/etcd-v3.5.3-linux-amd64.tar.gz

# 也可以从百度云盘下载
链接: https://pan.baidu.com/s/1eRrzyKk0VWBe8jSd0qdmYg 提取码: 6c7f
```

查看etcd集群的成员节点：

```bash
$ export ETCDCTL_API=3
$ etcdctl --endpoints=https://[127.0.0.1]:2379 --cacert=/etc/kubernetes/pki/etcd/ca.crt --cert=/etc/kubernetes/pki/etcd/healthcheck-client.crt --key=/etc/kubernetes/pki/etcd/healthcheck-client.key member list -w table

$ alias etcdctl='etcdctl --endpoints=https://[127.0.0.1]:2379 --cacert=/etc/kubernetes/pki/etcd/ca.crt --cert=/etc/kubernetes/pki/etcd/healthcheck-client.crt --key=/etc/kubernetes/pki/etcd/healthcheck-client.key'

$ etcdctl member list -w table
```

查看etcd集群节点状态：

```bash
$ etcdctl endpoint status -w table

$ etcdctl endpoint health -w table
```

设置key值:

```bash
$ etcdctl put luffy 1
$ etcdctl get luffy
```

查看所有key值：

```bash
$  etcdctl get / --prefix --keys-only
```

查看具体的key对应的数据：

```bash
$ etcdctl get /registry/pods/jenkins/sonar-postgres-7fc5d748b6-gtmsb
```

list-watch:

```bash
$ etcdctl watch /luffy/ --prefix
$ etcdctl put /luffy/key1 val1
```

添加定时任务做数据快照（重要！）

```bash
$ etcdctl snapshot save `hostname`-etcd_`date +%Y%m%d%H%M`.db
```

恢复快照：

1. 停止etcd和apiserver

2. 移走当前数据目录

   ```bash
   $ mv /var/lib/etcd/ /tmp
   ```

3. 恢复快照

   ```bash
   $ etcdctl snapshot restore `hostname`-etcd_`date +%Y%m%d%H%M`.db --data-dir=/var/lib/etcd/
   ```

4. 集群恢复

   https://github.com/etcd-io/etcd/blob/release-3.3/Documentation/op-guide/recovery.md

5. namespace删除问题

   很多情况下，会出现namespace删除卡住的问题，此时可以通过操作etcd来删除数据：

   ```bash
   # 查询namespace相关的元数据
   $ etcdctl get / --prefix --keys-only|grep namespace
   /registry/clusterrolebindings/system:controller:namespace-controller
   /registry/clusterroles/system:controller:namespace-controller
   /registry/namespaces/default
   /registry/namespaces/eladmin
   /registry/namespaces/kube-flannel
   /registry/namespaces/kube-node-lease
   /registry/namespaces/kube-public
   /registry/namespaces/kube-system
   /registry/namespaces/luffy
   /registry/serviceaccounts/kube-system/namespace-controller
   
   # 比如eladmin这个名称空间无法删除，则可以通过命令删除
   $ etcdctl delete /registry/namespaces/eladmin
   ```

###### [锦囊妙计](http://49.7.203.222:2023/#/kubernetes-advanced/etcd?id=锦囊妙计)

由于ETCD中存储了k8s集群全部的业务数据，考虑最坏的情况，当etcd节点的机器故障，机器无法恢复怎么办？

在新机器中将备份数据恢复至数据目录中：

```bash
export ETCDCTL_API=3
etcdctl snapshot restore k8s-master-etcd_202211052008.db --data-dir=/root/etcd/data
name="etcd-single"
host="172.21.65.227"
cluster="etcd1=http://172.21.65.227:2380"

docker run -d --privileged=true \
-p 2379:2379 \
-p 2380:2380 \
-v /root/etcd/data:/data/etcd \
--name $name \
--net=host \
quay.io/coreos/etcd:v3.5.0 \
/usr/local/bin/etcd \
--name $name  \
--data-dir /data/etcd \
--listen-client-urls  http://$host:2379 \
--advertise-client-urls http://$host:2379  \
--listen-peer-urls http://$host:2380 \
--initial-advertise-peer-urls http://$host:2380 \
--initial-cluster $cluster \
--initial-cluster-token=luffy  \
--initial-cluster-state=new \
--force-new-cluster  \
--log-level info \
--logger zap \
--log-outputs stderr


# 验证集群
export ETCDCTL_API=3
export ETCD_ENDPOINTS=172.21.65.227:2379
etcdctl --endpoints=$ETCD_ENDPOINTS -w table member list
etcdctl --endpoints=$ETCD_ENDPOINTS -w table endpoint status
etcdctl --endpoints=$ETCD_ENDPOINTS get / --prefix --keys-only
```

集群中某些特定的namespace被删除了数据，该如何增量恢复？

```bash
# 思路： 从备份中找到丢失的etcd数据，增量创建


# 找到丢失的数据，发现内容乱码
$ etcdctl --endpoints=$ETCD_ENDPOINTS get /registry/services/specs/luffy/mysql

# 使用etcdhelper直接返回json数据
# https://github.com/openshift/origin/tree/master/tools/etcdhelper
# 可以基于源码构建，也可以直接下载构建好的二进制文件

# 基于源码构建,由于源码比较大，github下载很慢，因此直接从下面网盘地址获取源码：
# 链接: https://pan.baidu.com/s/1zOv97hGyy-gCEBRqVsz1Yg 提取码: x8t7 

$ docker run -d --name go-builder  golang:1.17 sleep 30000
$ docker cp origin-master go-builder:/go
$ docker exec -ti go-builder bash
# cd /go/origin-master
# go env -w GOPROXY=https://goproxy.cn,direct
# CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build tools/etcdhelper/etcdhelper.go

$ docker cp go-builder:/go/origin-master/etcdhelper .
$ cp etcdhelper /usr/bin/


## 上述构建好的etcdhelper文件，也可以直接通过网盘下载：
## 链接: https://pan.baidu.com/s/1NJDy08nzuSlImAw5mXJZ-Q 提取码: 5i55
```

`etcdhelper`如何使用？

```bash
export ETCDCTL_API=3
export ETCD_ENDPOINTS=172.21.65.227:2379
etcdhelper -endpoint $ETCD_ENDPOINTS ls
etcdhelper -endpoint $ETCD_ENDPOINTS get /registry/services/specs/luffy/mysql
```

如何批量操作？

*kubectl没法直接通过json创建资源，因此需要将json文件保存且转换成为yaml格式*

```bash
# 需求：单独恢复luffy名称空间的资源

# 通过etcdctl或者luffy相关的资源存储的key
export ETCDCTL_API=3
export ETCD_ENDPOINTS=172.21.65.227:2379
etcdctl --endpoints=$ETCD_ENDPOINTS get / --prefix --keys-only|grep luffy >keys.txt

# 使用脚本利用etcdhelper将key转换成为json文件
cat key_to_json.sh
#!/bin/bash

i=0
export ETCDCTL_API=3
export ETCD_ENDPOINTS=172.21.65.227:2379
for line in `cat keys.txt`
do
   etcdhelper -endpoint $ETCD_ENDPOINTS   get $line >$i.json
   sed -i '1d' $i.json
   let 'i+=1'
done
```

有了json文件，需要将json转为yaml

```bash
docker exec -ti go-builder  bash
# git clone https://gitee.com/agagin/json2yaml-go.git
# go env -w GOPROXY=https://goproxy.cn,direct
# GO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -o json2yaml json2yaml.go
# pwd
# /go/src/json2yaml-go

docker cp go-builder:/go/src/json2yaml-go/json2yaml .

./json2yaml -jp .
```



# [Kubernetes调度器](http://49.7.203.222:2023/#/kubernetes-advanced/scheduler?id=kubernetes调度)

###### [为何要控制Pod应该如何调度](http://49.7.203.222:2023/#/kubernetes-advanced/scheduler?id=为何要控制pod应该如何调度)

- 集群中有些机器的配置高（SSD，更好的内存等），我们希望核心的服务（比如说数据库）运行在上面
- 某两个服务的网络传输很频繁，我们希望它们最好在同一台机器上
- ......

Kubernetes Scheduler 的作用是将待调度的 Pod 按照一定的调度算法和策略绑定到集群中一个合适的 Worker Node 上，并将绑定信息写入到 etcd 中，之后目标 Node 中 kubelet 服务通过 API Server 监听到 Scheduler 产生的 Pod 绑定事件获取 Pod 信息，然后下载镜像启动容器。

![img](4Kubernetes进阶实践.assets/kube-scheduler-1.jpg)

###### [调度的过程](http://49.7.203.222:2023/#/kubernetes-advanced/scheduler?id=调度的过程)

Scheduler 提供的调度流程分为预选 (Predicates) 和优选 (Priorities) 两个步骤：

- 预选，K8S会遍历当前集群中的所有 Node，筛选出其中符合要求的 Node 作为候选
- 优选，K8S将对候选的 Node 进行打分

经过预选筛选和优选打分之后，K8S选择分数最高的 Node 来运行 Pod，如果最终有多个 Node 的分数最高，那么 Scheduler 将从当中随机选择一个 Node 来运行 Pod。

![img](4Kubernetes进阶实践.assets/kube-scheduler-process.png)

预选：

![img](4Kubernetes进阶实践.assets/kube-scheduler-pre.jpg)

优选：

![img](4Kubernetes进阶实践.assets/kube-scheduler-pro.jpg)

###### [NodeSelector](http://49.7.203.222:2023/#/kubernetes-advanced/scheduler?id=nodeselector)

`label`是`kubernetes`中一个非常重要的概念，用户可以非常灵活的利用 label 来管理集群中的资源，POD 的调度可以根据节点的 label 进行特定的部署。

查看节点的label：

```bash
$ kubectl get nodes --show-labels
```

为节点打label：

```bash
$ kubectl label node k8s-master disktype=ssd
```

当 node 被打上了相关标签后，在调度的时候就可以使用这些标签了，只需要在spec 字段中添加`nodeSelector`字段，里面是我们需要被调度的节点的 label。

```yaml
...
spec:
  volumes: 
  - name: mysql-data
    hostPath: 
      path: /opt/mysql/data
  nodeSelector:   # 使用节点选择器将Pod调度到指定label的节点
    mysql: "true"
  containers:
  - name: mysql
      image: mysql:5.7
...
```

###### [nodeAffinity](http://49.7.203.222:2023/#/kubernetes-advanced/scheduler?id=nodeaffinity)

Pod -> Node的标签

节点亲和性 ， 比上面的`nodeSelector`更加灵活，它可以进行一些简单的逻辑组合，不只是简单的相等匹配 。分为两种，硬策略和软策略。

requiredDuringSchedulingIgnoredDuringExecution ： 硬策略，如果没有满足条件的节点的话，就不断重试直到满足条件为止，简单说就是你必须满足我的要求，不然我就不会调度Pod。

preferredDuringSchedulingIgnoredDuringExecution：软策略，如果你没有满足调度要求的节点的话，Pod就会忽略这条规则，继续完成调度过程，说白了就是满足条件最好了，没有满足就忽略掉的策略。

```yaml
#要求 Pod 不能运行在k8s-slave1和k8s-slave2两个节点上，如果有节点满足disktype=ssd或者sas的话就优先调度到这类节点上
...
spec:
      containers:
      - name: eladmin-api
        image: 172.21.65.226:5000/eladmin-api:v1
        ports:
        - containerPort: 8000
      affinity:
          nodeAffinity:
            requiredDuringSchedulingIgnoredDuringExecution:
                nodeSelectorTerms:
                - matchExpressions:
                    - key: kubernetes.io/hostname
                      operator: NotIn
                      values:
                        - k8s-slave1
                        - k8s-slave2
                        
            preferredDuringSchedulingIgnoredDuringExecution:
                - weight: 1
                  preference:
                    matchExpressions:
                    - key: disktype
                      operator: In
                      values:
                        - ssd
                        - sas
...
```

这里的匹配逻辑是 label 的值在某个列表中，现在`Kubernetes`提供的操作符有下面的几种：

- In：label 的值在某个列表中
- NotIn：label 的值不在某个列表中
- Gt：label 的值大于某个值
- Lt：label 的值小于某个值
- Exists：某个 label 存在
- DoesNotExist：某个 label 不存在

*如果nodeSelectorTerms下面有多个选项的话，满足任何一个条件就可以了；如果matchExpressions有多个选项的话，则必须同时满足这些条件才能正常调度 Pod*

###### [pod亲和性和反亲和性](http://49.7.203.222:2023/#/kubernetes-advanced/scheduler?id=pod亲和性和反亲和性)

Pod -> Pod的标签

场景：

> `eladmin-web`启动多副本，但是期望可以尽量分散到集群的可用节点中

分析：为了让`eladmin-web`应用的多个pod尽量分散部署在集群中，可以利用pod的反亲和性，告诉调度器，如果某个节点中存在了`eladmin-web`的pod，则可以根据实际情况，实现如下调度策略：

- 不允许同一个node节点，调度两个`eladmin-web`的副本
- 可以允许同一个node节点中调度两个`eladmin-web`的副本，前提是尽量把pod分散部署在集群中

```yaml
...
    spec:
      affinity:
        podAntiAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
          - labelSelector:
              matchExpressions:
              - key: app
                operator: In
                values:
                - eladmin-web
            topologyKey: kubernetes.io/hostname
      containers:
...
# 如果某个节点中，存在了app=eladmin-web的label的pod，那么 调度器一定不要给我调度过去

...
    spec:
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchExpressions:
                - key: app
                  operator: In
                  values:
                  - eladmin-web
              topologyKey: kubernetes.io/hostname
      containers:
...
# 如果某个节点中，存在了app=eladmin-web的label的pod，那么调度器尽量不要调度过去
```

> https://kubernetes.io/zh/docs/concepts/scheduling-eviction/assign-pod-node/

###### [污点（Taints）与容忍（tolerations）](http://49.7.203.222:2023/#/kubernetes-advanced/scheduler?id=污点（taints）与容忍（tolerations）)

对于`nodeAffinity`无论是硬策略还是软策略方式，都是调度 Pod 到预期节点上，而`Taints`恰好与之相反，如果一个节点标记为 Taints ，除非 Pod 也被标识为可以容忍污点节点，否则该 Taints 节点不会被调度Pod。

Taints(污点)是Node的一个属性，设置了Taints(污点)后，因为有了污点，所以Kubernetes是不会将Pod调度到这个Node上的。于是Kubernetes就给Pod设置了个属性Tolerations(容忍)，只要Pod能够容忍Node上的污点，那么Kubernetes就会忽略Node上的污点，就能够(不是必须)把Pod调度过去。

场景一：私有云服务中，某业务使用GPU进行大规模并行计算。为保证性能，希望确保该业务对服务器的专属性，避免将普通业务调度到部署GPU的服务器。

场景二：用户希望把 Master 节点保留给 Kubernetes 系统组件使用，或者把一组具有特殊资源预留给某些 Pod，则污点就很有用了，Pod 不会再被调度到 taint 标记过的节点。taint 标记节点举例如下：

设置污点：

```bash
$ kubectl taint node [node_name] key=value:[effect]   
      其中[effect] 可取值： [ NoSchedule | PreferNoSchedule | NoExecute ]
       NoSchedule：一定不能被调度。
       PreferNoSchedule：尽量不要调度。
       NoExecute：不仅不会调度，还会驱逐Node上已有的Pod。
  示例：kubectl taint node k8s-slave1 smoke=true:NoSchedule
```

去除污点：

```bash
去除指定key及其effect：
     kubectl taint nodes [node_name] key:[effect]-    #这里的key不用指定value
     kubectl taint node k8s-slave1 smoke-
 去除指定key所有的effect: 
     kubectl taint nodes node_name key-
 
 示例：
     kubectl taint node k8s-master smoke=true:NoSchedule
     kubectl taint node k8s-master smoke:NoExecute-
     kubectl taint node k8s-master smoke-
```

污点演示：

```bash
## 给k8s-slave1打上污点，smoke=true:NoSchedule
$ kubectl taint node k8s-master gamble=true:NoSchedule
$ kubectl taint node k8s-slave1 drunk=true:NoSchedule
$ kubectl taint node k8s-slave2 smoke=true:NoSchedule



## 扩容eladmin-web的Pod，观察新Pod的调度情况
$ kuebctl -n luffy scale deploy eladmin-web --replicas=3
$ kubectl -n luffy get po -w    ## pending
```

Pod容忍污点示例：

```bash
...
spec:
      containers:
      - name: eladmin-web
        image: 172.21.65.226:5000/eladmin/eladmin-web:v2
      tolerations: #设置容忍性
      - key: "smoke" 
        operator: "Equal"  #不指定operator，默认为Equal
        value: "true"
        effect: "NoSchedule"
      - key: "drunk" 
        operator: "Exists"  #如果操作符为Exists，那么value属性可省略,不指定operator，默认为Equal
      #意思是这个Pod要容忍的有污点的Node的key是smoke Equal true,效果是NoSchedule，
      #tolerations属性下各值必须使用引号，容忍的值都是设置Node的taints时给的值。
spec:
      containers:
      - name: eladmin-web
        image: 172.21.65.226:5000/eladmin/eladmin-web:v2
      tolerations:
        - operator: "Exists"
```

> NoExecute

###### [Cordon](http://49.7.203.222:2023/#/kubernetes-advanced/scheduler?id=cordon)

```bash
$ kubectl cordon k8s-slave2
$ kubectl drain k8s-slave2
```

###### [Pod驱逐策略](http://49.7.203.222:2023/#/kubernetes-advanced/scheduler?id=pod驱逐策略)

K8S 有个特色功能叫 pod eviction，它在某些场景下如节点 NotReady，或者资源不足时，把 pod 驱逐至其它节点，这也是出于业务保护的角度去考虑的。

1. Kube-controller-manager: 周期性检查所有节点状态，当节点处于 NotReady 状态超过一段时间后，驱逐该节点上所有 pod。

   - `pod-eviction-timeout`：NotReady 状态节点超过该时间后，执行驱逐，默认 5 min，适用于k8s 1.13版本之前

   - 1.13版本后，集群开启` TaintBasedEvictions 与TaintNodesByCondition` 功能，即[taint-based-evictions](https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/)，即节点若失联或者出现各种异常情况，k8s会自动为node打上污点，同时为pod默认添加如下容忍设置：

     ```yaml
       tolerations:
       - effect: NoExecute
         key: node.kubernetes.io/not-ready
         operator: Exists
         tolerationSeconds: 300
       - effect: NoExecute
         key: node.kubernetes.io/unreachable
         operator: Exists
         tolerationSeconds: 300
     ```

     即各pod可以独立设置驱逐容忍时间。

2. Kubelet: 周期性检查本节点资源，当资源不足时，按照优先级驱逐部分 pod

   - `memory.available`：节点可用内存
   - `nodefs.available`：节点根盘可用存储空间
   - `nodefs.inodesFree`：节点inodes可用数量
   - `imagefs.available`：镜像存储盘的可用空间
   - `imagefs.inodesFree`：镜像存储盘的inodes可用数量





# [Kubernetes认证与授权](http://49.7.203.222:2023/#/kubernetes-advanced/auth?id=kubernetes认证与授权)

###### [APIServer安全控制](http://49.7.203.222:2023/#/kubernetes-advanced/auth?id=apiserver安全控制)

![image-20221122085209765](4Kubernetes进阶实践.assets/image-20221122085209765.png)

- Authentication：身份认证

  1. 这个环节它面对的输入是整个`http request`，负责对来自client的请求进行身份校验，支持的方法包括:
     - `basic auth`
     - client证书验证（https双向验证）
     - `jwt token`(用于serviceaccount)
  2. APIServer启动时，可以指定一种Authentication方法，也可以指定多种方法。如果指定了多种方法，那么APIServer将会逐个使用这些方法对客户端请求进行验证， 只要请求数据通过其中一种方法的验证，APIServer就会认为Authentication成功；
  3. 使用kubeadm引导启动的k8s集群，apiserver的初始配置中，默认支持`client证书`验证和`serviceaccount`两种身份验证方式。 证书认证通过设置`--client-ca-file`根证书以及`--tls-cert-file`和`--tls-private-key-file`来开启。
  4. 在这个环节，apiserver会通过client证书或 `http header`中的字段(比如serviceaccount的`jwt token`)来识别出请求的`用户身份`，包括”user”、”group”等，这些信息将在后面的`authorization`环节用到。

- Authorization：鉴权，你可以访问哪些资源

  1. 这个环节面对的输入是`http request context`中的各种属性，包括：`user`、`group`、`request path`（比如：`/api/v1`、`/healthz`、`/version`等）、 `request verb`(比如：`get`、`list`、`create`等)。
  2. APIServer会将这些属性值与事先配置好的访问策略(`access policy`）相比较。APIServer支持多种`authorization mode`，包括`Node、RBAC、Webhook`等。
  3. APIServer启动时，可以指定一种`authorization mode`，也可以指定多种`authorization mode`，如果是后者，只要Request通过了其中一种mode的授权， 那么该环节的最终结果就是授权成功。在较新版本kubeadm引导启动的k8s集群的apiserver初始配置中，`authorization-mode`的默认配置是`”Node,RBAC”`。

- Admission Control：[准入控制](http://docs.kubernetes.org.cn/144.html)，一个控制链(层层关卡)，用于拦截请求的一种方式。偏集群安全控制、管理方面。

  - 为什么需要？

    认证与授权获取 http 请求 header 以及证书，无法通过body内容做校验。

    Admission 运行在 API Server 的增删改查 handler 中，可以自然地操作 API resource

  - 举个栗子

    - 以NamespaceLifecycle为例， 该插件确保处于Termination状态的Namespace不再接收新的对象创建请求，并拒绝请求不存在的Namespace。该插件还可以防止删除系统保留的Namespace:default，kube-system，kube-public

    - LimitRanger，若集群的命名空间设置了LimitRange对象，若Pod声明时未设置资源值，则按照LimitRange的定义来未Pod添加默认值

      ```yaml
      apiVersion: v1
      kind: LimitRange
      metadata:
        name: mem-limit-range
        namespace: demo
      spec:
        limits:
        - default:
            memory: 512Mi
          defaultRequest:
            memory: 256Mi
          type: Container
      ---
      apiVersion: v1
      kind: Pod
      metadata:
        name: default-mem-demo
        namespace: demo
      spec:
        containers:
        - name: default-mem-demo
          image: nginx:alpine
      ```

    ```bash
    $ kubectl apply -f .
    ```

- 怎么用？

  APIServer启动时通过 `--enable-admission-plugins --disable-admission-plugins` 指定需要打开或者关闭的 Admission Controller

- 场景

  - 自动注入sidecar容器或者initContainer容器
  - webhook admission，实现业务自定义的控制需求

###### [kubectl的认证授权](http://49.7.203.222:2023/#/kubernetes-advanced/auth?id=kubectl的认证授权)

kubectl的日志调试级别：

| 信息 | 描述                                                         |
| ---- | ------------------------------------------------------------ |
| v=0  | 通常，这对操作者来说总是可见的。                             |
| v=1  | 当您不想要很详细的输出时，这个是一个合理的默认日志级别。     |
| v=2  | 有关服务和重要日志消息的有用稳定状态信息，这些信息可能与系统中的重大更改相关。这是大多数系统推荐的默认日志级别。 |
| v=3  | 关于更改的扩展信息。                                         |
| v=4  | 调试级别信息。                                               |
| v=6  | 显示请求资源。                                               |
| v=7  | 显示 HTTP 请求头。                                           |
| v=8  | 显示 HTTP 请求内容。                                         |
| v=9  | 显示 HTTP 请求内容，并且不截断内容。                         |

```bash
$ kubectl get nodes -v=7
I0329 20:20:08.633065    3979 loader.go:359] Config loaded from file /root/.kube/config
I0329 20:20:08.633797    3979 round_trippers.go:416] GET https://172.21.51.143:6443/api/v1/nodes?limit=500
```

`kubeadm init`启动完master节点后，会默认输出类似下面的提示内容：

```bash
... ...
Your Kubernetes master has initialized successfully!

To start using your cluster, you need to run the following as a regular user:
  mkdir -p $HOME/.kube
  sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
  sudo chown $(id -u):$(id -g) $HOME/.kube/config
... ...
```

这些信息是在告知我们如何配置`kubeconfig`文件。按照上述命令配置后，master节点上的`kubectl`就可以直接使用`$HOME/.kube/config`的信息访问`k8s cluster`了。 并且，通过这种配置方式，`kubectl`也拥有了整个集群的管理员(root)权限。

很多K8s初学者在这里都会有疑问：

- 当`kubectl`使用这种`kubeconfig`方式访问集群时，`Kubernetes`的`kube-apiserver`是如何对来自`kubectl`的访问进行身份验证(`authentication`)和授权(`authorization`)的呢？
- 为什么来自`kubectl`的请求拥有最高的管理员权限呢？

查看`/root/.kube/config`文件：

前面提到过apiserver的authentication支持通过`tls client certificate、basic auth、token`等方式对客户端发起的请求进行身份校验， 从kubeconfig信息来看，kubectl显然在请求中使用了`tls client certificate`的方式，即客户端的证书。

证书base64解码：

```bash
$ echo xxxxxxxxxxxxxx |base64 -d > kubectl.crt
```

说明在认证阶段，`apiserver`会首先使用`--client-ca-file`配置的CA证书去验证kubectl提供的证书的有效性,基本的方式 ：

```bash
$  openssl verify -CAfile /etc/kubernetes/pki/ca.crt kubectl.crt
kubectl.crt: OK
```

除了认证身份，还会取出必要的信息供授权阶段使用，文本形式查看证书内容：

```bash
$ openssl x509 -in kubectl.crt -text
Certificate:
    Data:
        Version: 3 (0x2)
        Serial Number: 4736260165981664452 (0x41ba9386f52b74c4)
    Signature Algorithm: sha256WithRSAEncryption
        Issuer: CN=kubernetes
        Validity
            Not Before: Feb 10 07:33:39 2020 GMT
            Not After : Feb  9 07:33:40 2021 GMT
        Subject: O=system:masters, CN=kubernetes-admin
        ...
```

认证通过后，提取出签发证书时指定的CN(Common Name),`kubernetes-admin`，作为请求的用户名 (User Name), 从证书中提取O(Organization)字段作为请求用户所属的组 (Group)，`group = system:masters`，然后传递给后面的授权模块。

kubeadm在init初始引导集群启动过程中，创建了许多默认的RBAC规则， 在k8s有关RBAC的官方文档中，我们看到下面一些`default clusterrole`列表:

![img](4Kubernetes进阶实践.assets/kubeadm-default-clusterrole-list.png)

其中第一个cluster-admin这个cluster role binding绑定了system:masters group，这和authentication环节传递过来的身份信息不谋而合。 沿着system:masters group对应的cluster-admin clusterrolebinding“追查”下去，真相就会浮出水面。

我们查看一下这一binding：

```yaml
$ kubectl describe clusterrolebinding cluster-admin
Name:         cluster-admin
Labels:       kubernetes.io/bootstrapping=rbac-defaults
Annotations:  rbac.authorization.kubernetes.io/autoupdate: true
Role:
  Kind:  ClusterRole
  Name:  cluster-admin
Subjects:
  Kind   Name            Namespace
  ----   ----            ---------
  Group  system:masters
```

我们看到在kube-system名字空间中，一个名为cluster-admin的clusterrolebinding将cluster-admin cluster role与system:masters Group绑定到了一起， 赋予了所有归属于system:masters Group中用户cluster-admin角色所拥有的权限。

我们再来查看一下cluster-admin这个role的具体权限信息：

```bash
$ kubectl describe clusterrole cluster-admin
Name:         cluster-admin
Labels:       kubernetes.io/bootstrapping=rbac-defaults
Annotations:  rbac.authorization.kubernetes.io/autoupdate: true
PolicyRule:
  Resources  Non-Resource URLs  Resource Names  Verbs
  ---------  -----------------  --------------  -----
  *.*        []                 []              [*]
             [*]                []              [*]
```

非资源类，如查看集群健康状态。

![img](4Kubernetes进阶实践.assets/how-kubectl-be-authorized.png)

###### [RBAC](http://49.7.203.222:2023/#/kubernetes-advanced/auth?id=rbac)

Role-Based Access Control，基于角色的访问控制， apiserver启动参数添加--authorization-mode=RBAC 来启用RBAC认证模式，kubeadm安装的集群默认已开启。[官方介绍](https://kubernetes.io/docs/reference/access-authn-authz/rbac/)

查看开启：

```bash
# master节点查看apiserver进程
$ ps aux |grep apiserver
```

RBAC模式引入了4个资源类型：

- Role，角色

  一个Role只能授权访问单个namespace

  ```yaml
  ## 示例定义一个名为pod-reader的角色，该角色具有读取demo这个命名空间下的pods的权限
  kind: Role
  apiVersion: rbac.authorization.k8s.io/v1
  metadata:
    namespace: demo
    name: pod-reader
  rules:
  - apiGroups: [""] # "" indicates the core API group
    resources: ["pods"]
    verbs: ["get", "watch", "list"]
    
  ## apiGroups: "","apps", "autoscaling", "batch", kubectl api-versions
  ## resources: "services", "pods","deployments"... kubectl api-resources
  ## verbs: "get", "list", "watch", "create", "update", "patch", "delete", "exec"
  
  ## https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.19/
  ```

- ClusterRole

  一个ClusterRole能够授予和Role一样的权限，但是它是集群范围内的。

  ```yaml
  ## 定义一个集群角色，名为secret-reader，该角色可以读取所有的namespace中的secret资源
  kind: ClusterRole
  apiVersion: rbac.authorization.k8s.io/v1
  metadata:
    # "namespace" omitted since ClusterRoles are not namespaced
    name: secret-reader
  rules:
  - apiGroups: [""]
    resources: ["secrets"]
    verbs: ["get", "watch", "list"]
  
  # User,Group,ServiceAccount
  ```

- Rolebinding

  将role中定义的权限分配给用户和用户组。RoleBinding包含主题（users,groups,或service accounts）和授予角色的引用。对于namespace内的授权使用RoleBinding，集群范围内使用ClusterRoleBinding。

  ```yaml
  ## 定义一个角色绑定，将pod-reader这个role的权限授予给luffy这个User，使得luffy可以在读取default这个命名空间下的所有的pod数据
  kind: RoleBinding
  apiVersion: rbac.authorization.k8s.io/v1
  metadata:
    name: read-pods
    namespace: demo
  subjects:
  - kind: User   #这里可以是User,Group,ServiceAccount
    name: luffy
    apiGroup: rbac.authorization.k8s.io
  roleRef:
    kind: Role #这里可以是Role或者ClusterRole,若是ClusterRole，则权限也仅限于rolebinding的内部
    name: pod-reader # match the name of the Role or ClusterRole you wish to bind to
    apiGroup: rbac.authorization.k8s.io
  ```

*注意：rolebinding既可以绑定role，也可以绑定clusterrole，当绑定clusterrole的时候，subject的权限也会被限定于rolebinding定义的namespace内部，若想跨namespace，需要使用clusterrolebinding*

```yaml
  ## 定义一个角色绑定，将dave这个用户和secret-reader这个集群角色绑定，虽然secret-reader是集群角色，但是因为是使用rolebinding绑定的，因此dave的权限也会被限制在development这个命名空间内
  apiVersion: rbac.authorization.k8s.io/v1
  kind: RoleBinding
  metadata:
    name: read-secrets
    namespace: development
  subjects:
  - kind: User
    name: dave # Name is case sensitive
    apiGroup: rbac.authorization.k8s.io
  - kind: ServiceAccount
    name: dave # Name is case sensitive
    namespace: luffy
  roleRef:
    kind: ClusterRole
    name: secret-reader
    apiGroup: rbac.authorization.k8s.io
```

考虑一个场景： 如果集群中有多个namespace分配给不同的管理员，每个namespace的权限是一样的，就可以只定义一个clusterrole，然后通过rolebinding将不同的namespace绑定到管理员身上，否则就需要每个namespace定义一个Role，然后做一次rolebinding。

- ClusterRolebingding

  允许跨namespace进行授权

  ```yaml
  apiVersion: rbac.authorization.k8s.io/v1
  kind: ClusterRoleBinding
  metadata:
    name: read-secrets-global
  subjects:
  - kind: Group
    name: manager # Name is case sensitive
    apiGroup: rbac.authorization.k8s.io
  roleRef:
    kind: ClusterRole
    name: secret-reader
    apiGroup: rbac.authorization.k8s.io
  ```

![img](4Kubernetes进阶实践.assets/rbac-2.jpg)

###### [kubelet的认证授权](http://49.7.203.222:2023/#/kubernetes-advanced/auth?id=kubelet的认证授权)

查看kubelet进程

```bash
$ systemctl status kubelet
● kubelet.service - kubelet: The Kubernetes Node Agent
   Loaded: loaded (/usr/lib/systemd/system/kubelet.service; enabled; vendor preset: disabled)
  Drop-In: /usr/lib/systemd/system/kubelet.service.d
           └─10-kubeadm.conf
   Active: active (running) since Sun 2020-07-05 19:33:36 EDT; 1 day 12h ago
     Docs: https://kubernetes.io/docs/
 Main PID: 10622 (kubelet)
    Tasks: 24
   Memory: 60.5M
   CGroup: /system.slice/kubelet.service
           └─851 /usr/bin/kubelet --bootstrap-kubeconfig=/etc/kubernetes/bootstrap-kubelet.conf --kubeconfig=/etc/kubernetes/kubelet.conf
```

查看`/etc/kubernetes/kubelet.conf`，解析证书：

```bash
$ echo xxxxx |base64 -d >kubelet.crt
$ openssl x509 -in kubelet.crt -text
Certificate:
    Data:
        Version: 3 (0x2)
        Serial Number: 9059794385454520113 (0x7dbadafe23185731)
    Signature Algorithm: sha256WithRSAEncryption
        Issuer: CN=kubernetes
        Validity
            Not Before: Feb 10 07:33:39 2020 GMT
            Not After : Feb  9 07:33:40 2021 GMT
        Subject: O=system:nodes, CN=system:node:master-1
```

得到我们期望的内容：

```bash
Subject: O=system:nodes, CN=system:node:k8s-master
```

我们知道，k8s会把O作为Group来进行请求，因此如果有权限绑定给这个组，肯定在clusterrolebinding的定义中可以找得到。因此尝试去找一下绑定了system:nodes组的clusterrolebinding

```bash
$ kubectl get clusterrolebinding -oyaml|grep -n10 system:nodes
178-    resourceVersion: "225"
179-    selfLink: /apis/rbac.authorization.k8s.io/v1/clusterrolebindings/kubeadm%3Anode-autoapprove-certificate-rotation
180-    uid: b4303542-d383-4b62-a1e9-02f2cefa2c20
181-  roleRef:
182-    apiGroup: rbac.authorization.k8s.io
183-    kind: ClusterRole
184-    name: system:certificates.k8s.io:certificatesigningrequests:selfnodeclient
185-  subjects:
186-  - apiGroup: rbac.authorization.k8s.io
187-    kind: Group
188:    name: system:nodes
189-- apiVersion: rbac.authorization.k8s.io/v1
190-  kind: ClusterRoleBinding
191-  metadata:
192-    creationTimestamp: "2021-06-06T02:39:46Z"
193-    managedFields:
194-    - apiVersion: rbac.authorization.k8s.io/v1
195-      fieldsType: FieldsV1
196-      fieldsV1:
197-        f:roleRef:
198-          f:apiGroup: {}

$ kubectl describe clusterrole system:certificates.k8s.io:certificatesigningrequests:selfnodeclient
Name:         system:certificates.k8s.io:certificatesigningrequests:selfnodeclient
Labels:       kubernetes.io/bootstrapping=rbac-defaults
Annotations:  rbac.authorization.kubernetes.io/autoupdate: true
PolicyRule:
  Resources                                                      Non-Resource URLs  Resource Names  Verbs
  ---------                                                      -----------------  --------------  -----
  certificatesigningrequests.certificates.k8s.io/selfnodeclient  []                 []              [create]
```

结局有点意外，除了`system:certificates.k8s.io:certificatesigningrequests:selfnodeclient`外，没有找到system相关的rolebindings，显然和我们的理解不一样。 尝试去找[资料](https://kubernetes.io/docs/reference/access-authn-authz/rbac/#core-component-roles)，发现了这么一段 :

| Default ClusterRole            | Default ClusterRoleBinding          | Description                                                  |
| ------------------------------ | ----------------------------------- | ------------------------------------------------------------ |
| system:kube-scheduler          | system:kube-scheduler user          | Allows access to the resources required by the [scheduler](https://kubernetes.io/docs/reference/generated/kube-scheduler/)component. |
| system:volume-scheduler        | system:kube-scheduler user          | Allows access to the volume resources required by the kube-scheduler component. |
| system:kube-controller-manager | system:kube-controller-manager user | Allows access to the resources required by the [controller manager](https://kubernetes.io/docs/reference/command-line-tools-reference/kube-controller-manager/) component. The permissions required by individual controllers are detailed in the [controller roles](https://kubernetes.io/docs/reference/access-authn-authz/rbac/#controller-roles). |
| system:node                    | None                                | Allows access to resources required by the kubelet, **including read access to all secrets, and write access to all pod status objects**. You should use the [Node authorizer](https://kubernetes.io/docs/reference/access-authn-authz/node/) and [NodeRestriction admission plugin](https://kubernetes.io/docs/reference/access-authn-authz/admission-controllers/#noderestriction) instead of the `system:node` role, and allow granting API access to kubelets based on the Pods scheduled to run on them. The `system:node` role only exists for compatibility with Kubernetes clusters upgraded from versions prior to v1.8. |
| system:node-proxier            | system:kube-proxy user              | Allows access to the resources required by the [kube-proxy](https://kubernetes.io/docs/reference/command-line-tools-reference/kube-proxy/)component. |

大致意思是说：之前会定义system:node这个角色，目的是为了kubelet可以访问到必要的资源，包括所有secret的读权限及更新pod状态的写权限。如果1.8版本后，是建议使用 [Node authorizer](https://kubernetes.io/docs/reference/access-authn-authz/node/) and [NodeRestriction admission plugin](https://kubernetes.io/docs/reference/access-authn-authz/admission-controllers/#noderestriction) 来代替这个角色的。

查看一下授权策略：

```bash
$ ps axu|grep apiserver
kube-apiserver --authorization-mode=Node,RBAC  --enable-admission-plugins=NodeRestriction
```

查看一下官网对Node authorizer的介绍：

*Node authorization is a special-purpose authorization mode that specifically authorizes API requests made by kubelets.*

*In future releases, the node authorizer may add or remove permissions to ensure kubelets have the minimal set of permissions required to operate correctly.*

*In order to be authorized by the Node authorizer, kubelets must use a credential that identifies them as being in the `system:nodes` group, with a username of `system:node:<nodeName>`*

###### [创建用户认证授权的kubeconfig文件](http://49.7.203.222:2023/#/kubernetes-advanced/auth?id=创建用户认证授权的kubeconfig文件)

签发证书对：

```bash
# 生成私钥
$ openssl genrsa -out luffy.key 2048

# 生成证书请求文件
$ openssl req -new -key luffy.key -out luffy.csr -subj "/O=admin:luffy/CN=luffy-admin"

# 证书拓展属性
$ cat extfile.conf
[ v3_ca ]
keyUsage = critical, digitalSignature, keyEncipherment
extendedKeyUsage = clientAuth

# 生成luffy.crt证书
$ openssl x509 -req -in luffy.csr -CA /etc/kubernetes/pki/ca.crt -CAkey /etc/kubernetes/pki/ca.key -CAcreateserial -sha256 -out luffy.crt -extensions v3_ca -extfile extfile.conf -days 3650
```

配置kubeconfig文件：

```bash
# 创建kubeconfig文件，指定集群名称和地址
$ kubectl config set-cluster luffy-cluster --certificate-authority=/etc/kubernetes/pki/ca.crt --embed-certs=true --server=https://172.21.65.226:6443 --kubeconfig=luffy.kubeconfig

# 为kubeconfig文件添加认证信息
$ kubectl config set-credentials luffy-admin --client-certificate=luffy.crt --client-key=luffy.key --embed-certs=true --kubeconfig=luffy.kubeconfig

# 为kubeconfig添加上下文配置
$ kubectl config set-context luffy-context --cluster=luffy-cluster --user=luffy-admin --kubeconfig=luffy.kubeconfig

# 设置默认的上下文
$ kubectl config use-context luffy-context --kubeconfig=luffy.kubeconfig
```

验证：

```bash
# 设置当前kubectl使用的config文件
$ export KUBECONFIG=luffy.kubeconfig

# 当前不具有任何权限，因为没有为用户或者组设置RBAC规则
$ kubectl get po
Error from server (Forbidden): pods is forbidden: User "luffy-admin" cannot list resource "pods" in API group "" in the namespace "default"
```

为luffy-admin用户添加luffy命名空间访问权限：

```bash
# 定义role，具有luffy命名空间的所有权限
$ cat luffy-admin-role.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: luffy
  name: luffy-admin
rules:
- apiGroups: ["*"] # "" 指定核心 API 组
  resources: ["*"]
  verbs: ["*"]
  
#定义rolebinding，为luffy用户绑定luffy-admin这个role，这样luffy用户就有操作luffy命名空间的所有权限
$ cat luffy-admin-rolebinding.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: luffy-admin
  namespace: luffy
subjects:
- kind: User
  name: luffy-admin # Name is case sensitive
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role #this must be Role or ClusterRole
  name: luffy-admin # 这里的名称必须与你想要绑定的 Role 或 ClusterRole 名称一致
  apiGroup: rbac.authorization.k8s.io
```

###### [Service Account及K8S Api调用](http://49.7.203.222:2023/#/kubernetes-advanced/auth?id=service-account及k8s-api调用)

前面说，认证可以通过证书，也可以通过使用ServiceAccount（服务账户）的方式来做认证。大多数时候，我们在基于k8s做二次开发时都是选择通过ServiceAccount + RBAC 的方式。

*思考：ingress-nginx-controller 需要监听ingress资源，权限如何获取？*

```bash
# 查看ingress-nginx-controller的deployment
kubectl -n ingress-nginx get deployment ingress-nginx-controller -oyaml
...
      dnsPolicy: ClusterFirst
      hostNetwork: true
      nodeSelector:
        ingress: "true"
        kubernetes.io/os: linux
      restartPolicy: Always
      schedulerName: default-scheduler
      securityContext: {}
      serviceAccount: ingress-nginx
      serviceAccountName: ingress-nginx
      terminationGracePeriodSeconds: 300
      volumes:
      - name: webhook-cert
        secret:
          defaultMode: 420
          secretName: ingress-nginx-admission
...
```

发现指定了serviceAccountName，前面我们知道`role`或者`clusterrole`可以授予的对象中包含：

- User
- Group
- ServiceAccount

因此，猜测应该是部署`ingress-nginx-controller`的时候，创建了相应的RBAC规则。

```bash
$ kubectl describe clusterrole ingress-nginx
Name:         ingress-nginx
Labels:       app.kubernetes.io/instance=ingress-nginx
              app.kubernetes.io/name=ingress-nginx
              app.kubernetes.io/part-of=ingress-nginx
              app.kubernetes.io/version=1.4.0
Annotations:  <none>
PolicyRule:
  Resources                           Non-Resource URLs  Resource Names  Verbs
  ---------                           -----------------  --------------  -----
  events                              []                 []              [create patch]
  services                            []                 []              [get list watch]
  ingressclasses.networking.k8s.io    []                 []              [get list watch]
  ingresses.networking.k8s.io         []                 []              [get list watch]
  nodes                               []                 []              [list watch get]
  endpointslices.discovery.k8s.io     []                 []              [list watch get]
  configmaps                          []                 []              [list watch]
  endpoints                           []                 []              [list watch]
  namespaces                          []                 []              [list watch]
  pods                                []                 []              [list watch]
  secrets                             []                 []              [list watch]
  leases.coordination.k8s.io          []                 []              [list watch]
  ingresses.networking.k8s.io/status  []                 []              [update]
```

*思考：如何使用ServiceAccount调用k8s的接口？*

```bash
$ kubectl -n ingress-nginx exec -ti ingress-nginx-controller-555746c4b4-cwwg9 -- bash
bash-5.1$ df -h
Filesystem                Size      Used Available Use% Mounted on
overlay                  74.0G      9.6G     64.4G  13% /
tmpfs                    64.0M         0     64.0M   0% /dev
tmpfs                     7.8G         0      7.8G   0% /sys/fs/cgroup
shm                      64.0M         0     64.0M   0% /dev/shm
/dev/sda3                74.0G      9.6G     64.4G  13% /etc/hosts
/dev/sda3                74.0G      9.6G     64.4G  13% /dev/termination-log
/dev/sda3                74.0G      9.6G     64.4G  13% /etc/hostname
/dev/sda3                74.0G      9.6G     64.4G  13% /etc/resolv.conf
tmpfs                    15.4G     12.0K     15.4G   0% /usr/local/certificates
tmpfs                    15.4G     12.0K     15.4G   0% /run/secrets/kubernetes.io/serviceaccount
tmpfs                     7.8G         0      7.8G   0% /proc/acpi
tmpfs                    64.0M         0     64.0M   0% /proc/kcore
tmpfs                    64.0M         0     64.0M   0% /proc/keys
tmpfs                    64.0M         0     64.0M   0% /proc/timer_list
tmpfs                    64.0M         0     64.0M   0% /proc/timer_stats
tmpfs                    64.0M         0     64.0M   0% /proc/sched_debug
tmpfs                     7.8G         0      7.8G   0% /proc/scsi
tmpfs                     7.8G         0      7.8G   0% /sys/firmware

cat /run/secrets/kubernetes.io/serviceaccount/token
eyJhbGciOiJSUzI1NiIsImtpZCI6IktJeWtHUFlydXZ2ZncxQVNxUlZyWHhCTkkwb01IbjNKUnFwZ18wUUxkVGcifQ.eyJhdWQiOlsiaHR0cHM6Ly9rdWJlcm5ldGVzLmRlZmF1bHQuc3ZjLmNsdXN0ZXIubG9jYWwiXSwiZXhwIjoxNjk5Njk2MjI3LCJpYXQiOjE2NjgxNjAyMjcsImlzcyI6Imh0dHBzOi8va3ViZXJuZXRlcy5kZWZhdWx0LnN2Yy5jbHVzdGVyLmxvY2FsIiwia3ViZXJuZXRlcy5pbyI6eyJuYW1lc3BhY2UiOiJpbmdyZXNzLW5naW54IiwicG9kIjp7Im5hbWUiOiJpbmdyZXNzLW5naW54LWNvbnRyb2xsZXItNTU1NzQ2YzRiNC1jd3dnOSIsInVpZCI6ImY4NjEzNjI3LWQyNWItNDU5MC05NjNmLTZhNGZhNDBmODJhNyJ9LCJzZXJ2aWNlYWNjb3VudCI6eyJuYW1lIjoiaW5ncmVzcy1uZ2lueCIsInVpZCI6ImJhMDNjODQyLWM4MDctNDY3My05NzRmLTA2ZWM2ZjA5MTE3YiJ9LCJ3YXJuYWZ0ZXIiOjE2NjgxNjM4MzR9LCJuYmYiOjE2NjgxNjAyMjcsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDppbmdyZXNzLW5naW54OmluZ3Jlc3MtbmdpbngifQ.iCPjYEi_x2WWpAF4X5uEfgxG0eGeQ5hoVPTR8c6xgHkm2SpAuBHk1bf6jQgJO_UJZ5rM-DP2hkK2wETNtXnWi3k5bt5HrXcIIZrGwh9UC8D1mMGJbQ0oUkmLr9wvvwtj153AzBtkS7KFn5j0PWx987HcCyRmEtr06QSnLH7-1Y29n9AYYOlNHTUpUDyN8v-zLDA_Oua6qQPf8oHgpTSd7M-LQXAumFUNCi50l9FI2RdPsQG8ko0vKAAqESf9pML_qbMQpwOjYlCfB0quDb6WAbvtvsj1IKwlF7dlymzUJKCqiF8ZVq5VNuQS8FhlVt1G5B1N9M7luPcGTCzQq6wmFQ
```

Pod中若指定了`serviceAccount`，则k8s自动为Pod挂载`/run/secrets/kubernetes.io/serviceaccount/token`这个文件，文件内容为token信息，业务程序可以使用该token进行k8s api的调用，同时，该token的访问权限与对应的`serviceAccount`的权限一致。

```bash
curl -k  -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IktJeWtHUFlydXZ2ZncxQVNxUlZyWHhCTkkwb01IbjNKUnFwZ18wUUxkVGcifQ.eyJhdWQiOlsiaHR0cHM6Ly9rdWJlcm5ldGVzLmRlZmF1bHQuc3ZjLmNsdXN0ZXIubG9jYWwiXSwiZXhwIjoxNjk5Njk2MjI3LCJpYXQiOjE2NjgxNjAyMjcsImlzcyI6Imh0dHBzOi8va3ViZXJuZXRlcy5kZWZhdWx0LnN2Yy5jbHVzdGVyLmxvY2FsIiwia3ViZXJuZXRlcy5pbyI6eyJuYW1lc3BhY2UiOiJpbmdyZXNzLW5naW54IiwicG9kIjp7Im5hbWUiOiJpbmdyZXNzLW5naW54LWNvbnRyb2xsZXItNTU1NzQ2YzRiNC1jd3dnOSIsInVpZCI6ImY4NjEzNjI3LWQyNWItNDU5MC05NjNmLTZhNGZhNDBmODJhNyJ9LCJzZXJ2aWNlYWNjb3VudCI6eyJuYW1lIjoiaW5ncmVzcy1uZ2lueCIsInVpZCI6ImJhMDNjODQyLWM4MDctNDY3My05NzRmLTA2ZWM2ZjA5MTE3YiJ9LCJ3YXJuYWZ0ZXIiOjE2NjgxNjM4MzR9LCJuYmYiOjE2NjgxNjAyMjcsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDppbmdyZXNzLW5naW54OmluZ3Jlc3MtbmdpbngifQ.iCPjYEi_x2WWpAF4X5uEfgxG0eGeQ5hoVPTR8c6xgHkm2SpAuBHk1bf6jQgJO_UJZ5rM-DP2hkK2wETNtXnWi3k5bt5HrXcIIZrGwh9UC8D1mMGJbQ0oUkmLr9wvvwtj153AzBtkS7KFn5j0PWx987HcCyRmEtr06QSnLH7-1Y29n9AYYOlNHTUpUDyN8v-zLDA_Oua6qQPf8oHgpTSd7M-LQXAumFUNCi50l9FI2RdPsQG8ko0vKAAqESf9pML_qbMQpwOjYlCfB0quDb6WAbvtvsj1IKwlF7dlymzUJKCqiF8ZVq5VNuQS8FhlVt1G5B1N9M7luPcGTCzQq6wmFQ" https://172.21.65.226:6443/api/v1/nodes
```

![img](4Kubernetes进阶实践.assets/rbac.jpg)

只允许访问luffy命名空间的pod资源：

```bash
$ cat luffy-admin-rbac.yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: luffy-pods-admin
  namespace: luffy

---
kind: Role
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  namespace: luffy
  name: pods-reader-writer
rules:
- apiGroups: ["*"] # "" indicates the core API group
  resources: ["pods"]
  verbs: ["*"]
---
kind: RoleBinding
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: pods-reader-writer
  namespace: luffy
subjects:
- kind: ServiceAccount   #这里可以是User,Group,ServiceAccount
  name: luffy-pods-admin
  namespace: luffy
roleRef:
  kind: Role #这里可以是Role或者ClusterRole,若是ClusterRole，则权限也仅限于rolebinding的内部
  name: pods-reader-writer
  apiGroup: rbac.authorization.k8s.io
```

演示权限：

```bash
$ kubectl -n luffy create token luffy-pods-admin
eyJhbGciOiJSUzI1NiIsImtpZCI6IktJeWtHUFlydXZ2ZncxQVNxUlZyWHhCTkkwb01IbjNKUnFwZ18wUUxkVGcifQ.eyJhdWQiOlsiaHR0cHM6Ly9rdWJlcm5ldGVzLmRlZmF1bHQuc3ZjLmNsdXN0ZXIubG9jYWwiXSwiZXhwIjoxNjY4MTY2MDYxLCJpYXQiOjE2NjgxNjI0NjEsImlzcyI6Imh0dHBzOi8va3ViZXJuZXRlcy5kZWZhdWx0LnN2Yy5jbHVzdGVyLmxvY2FsIiwia3ViZXJuZXRlcy5pbyI6eyJuYW1lc3BhY2UiOiJsdWZmeSIsInNlcnZpY2VhY2NvdW50Ijp7Im5hbWUiOiJsdWZmeS1wb2RzLWFkbWluIiwidWlkIjoiZGY3ZjRiZTAtMTI2Yy00ZTExLWJlNWYtZWZhYjk4NGY2OWZkIn19LCJuYmYiOjE2NjgxNjI0NjEsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDpsdWZmeTpsdWZmeS1wb2RzLWFkbWluIn0.ZVO9smO5milPXJWkA9YLeSNMTBTNbqHFyO2YJipQ0BGAlTRkprsfnnS6Xod-1nP2bQmb1xdDiLhi2lhqoAGiornfV573eggbuYdB-xgqnD9cFP-PZzzUJ3G5Up-CUtkjO6kY1ljUa5s8TuTfqIpkbniaKUPciZSgLy4ozRbjOotrnZqpw6dKIuDRBFl26CvztNf3LvxinbeWeJv1dRPHzi90qKEopx2HR3PHBrcs7NuHk5c0He7Bjs1RsVvL1uOVYLXLIYgcnIZra1W8uMcff4-klinEYFo_g_CszTYx-MGLPcSLaHMcNw_qmXsVeq92JA-EooSDzF8XRQqZyLAe2g
$ curl -k  -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IktJeWtHUFlydXZ2ZncxQVNxUlZyWHhCTkkwb01IbjNKUnFwZ18wUUxkVGcifQ.eyJhdWQiOlsiaHR0cHM6Ly9rdWJlcm5ldGVzLmRlZmF1bHQuc3ZjLmNsdXN0ZXIubG9jYWwiXSwiZXhwIjoxNjY4MTY2MDYxLCJpYXQiOjE2NjgxNjI0NjEsImlzcyI6Imh0dHBzOi8va3ViZXJuZXRlcy5kZWZhdWx0LnN2Yy5jbHVzdGVyLmxvY2FsIiwia3ViZXJuZXRlcy5pbyI6eyJuYW1lc3BhY2UiOiJsdWZmeSIsInNlcnZpY2VhY2NvdW50Ijp7Im5hbWUiOiJsdWZmeS1wb2RzLWFkbWluIiwidWlkIjoiZGY3ZjRiZTAtMTI2Yy00ZTExLWJlNWYtZWZhYjk4NGY2OWZkIn19LCJuYmYiOjE2NjgxNjI0NjEsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDpsdWZmeTpsdWZmeS1wb2RzLWFkbWluIn0.ZVO9smO5milPXJWkA9YLeSNMTBTNbqHFyO2YJipQ0BGAlTRkprsfnnS6Xod-1nP2bQmb1xdDiLhi2lhqoAGiornfV573eggbuYdB-xgqnD9cFP-PZzzUJ3G5Up-CUtkjO6kY1ljUa5s8TuTfqIpkbniaKUPciZSgLy4ozRbjOotrnZqpw6dKIuDRBFl26CvztNf3LvxinbeWeJv1dRPHzi90qKEopx2HR3PHBrcs7NuHk5c0He7Bjs1RsVvL1uOVYLXLIYgcnIZra1W8uMcff4-klinEYFo_g_CszTYx-MGLPcSLaHMcNw_qmXsVeq92JA-EooSDzF8XRQqZyLAe2g" https://172.21.65.226:6443/api/v1/namespaces/luffy/pods?limit=500

# https://172.21.65.226:6443/api/v1/nodes
```

###### [认证、鉴权图鉴](http://49.7.203.222:2023/#/kubernetes-advanced/auth?id=认证、鉴权图鉴)

![img](4Kubernetes进阶实践.assets/AUTH.jpg)





# [通过HPA实现业务应用的动态扩缩容](http://49.7.203.222:2023/#/kubernetes-advanced/hpa?id=通过hpa实现业务应用的动态扩缩容)

##### [HPA控制器介绍](http://49.7.203.222:2023/#/kubernetes-advanced/hpa?id=hpa控制器介绍)

当系统资源过高的时候，我们可以使用如下命令来实现 Pod 的扩缩容功能

```bash
$ kubectl -n luffy scale deployment eladmin-web --replicas=2
```

但是这个过程是手动操作的。在实际项目中，我们需要做到是的是一个自动化感知并自动扩容的操作。Kubernetes 也为提供了这样的一个资源对象：Horizontal Pod Autoscaling（Pod 水平自动伸缩），简称[HPA](https://v1-14.docs.kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/)

![img](4Kubernetes进阶实践.assets/hpa2.jpg)

基本原理：HPA 通过监控分析控制器控制的所有 Pod 的负载变化情况来确定是否需要调整 Pod 的副本数量

##### [Metric Server](http://49.7.203.222:2023/#/kubernetes-advanced/hpa?id=metric-server)

[官方介绍](https://v1-14.docs.kubernetes.io/docs/tasks/debug-application-cluster/resource-metrics-pipeline/#metrics-server)

```
...
Metric server collects metrics from the Summary API, exposed by Kubelet on each node.

Metrics Server registered in the main API server through Kubernetes aggregator, which was introduced in Kubernetes 1.7
...
```

###### [安装](http://49.7.203.222:2023/#/kubernetes-advanced/hpa?id=安装)

官方代码仓库地址：https://github.com/kubernetes-sigs/metrics-server

Depending on your cluster setup, you may also need to change flags passed to the Metrics Server container. Most useful flags:

- `--kubelet-preferred-address-types` - The priority of node address types used when determining an address for connecting to a particular node (default [Hostname,InternalDNS,InternalIP,ExternalDNS,ExternalIP])
- `--kubelet-insecure-tls` - Do not verify the CA of serving certificates presented by Kubelets. For testing purposes only.
- `--requestheader-client-ca-file` - Specify a root certificate bundle for verifying client certificates on incoming requests.

```bash
$ wget https://github.com/kubernetes-sigs/metrics-server/releases/download/v0.6.1/components.yaml
```

修改args参数：

```bash
# 添加- --kubelet-insecure-tls
...
133       containers:
134       - args:
135         - --cert-dir=/tmp
136         - --secure-port=4443
            - --kubelet-insecure-tls
137         - --kubelet-preferred-address-types=InternalIP,ExternalIP,Hostname
138         - --kubelet-use-node-status-port
139         - --metric-resolution=15s
140         image: bitnami/metrics-server:0.6.1
141         imagePullPolicy: IfNotPresent
...
```

执行安装：

```bash
$ kubectl apply -f components.yaml

$ kubectl -n kube-system get pods

$ kubectl top nodes
```

##### [HPA实践](http://49.7.203.222:2023/#/kubernetes-advanced/hpa?id=hpa实践)

HPA的实现有两个版本：

- autoscaling/v1，只包含了根据CPU指标的检测，稳定版本
- autoscaling/v2，支持根据cpu、memory或者用户自定义指标进行伸缩

###### [基于CPU和内存的动态伸缩](http://49.7.203.222:2023/#/kubernetes-advanced/hpa?id=基于cpu和内存的动态伸缩)

![img](4Kubernetes进阶实践.assets/hpa.png)

创建hpa对象：

```bash
# 方式一
$ cat hpa-eladmin-web.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: hpa-eladmin-web
  namespace: luffy
spec:
  maxReplicas: 3
  minReplicas: 1
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: eladmin-web
  metrics:
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 80
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 80

# 方式二
$ kubectl -n luffy autoscale deployment eladmin-web --cpu-percent=80 --min=1 --max=3
```

> Deployment对象必须配置requests的参数，不然无法获取监控数据，也无法通过HPA进行动态伸缩

验证：

```bash
$ yum -y install httpd-tools
$ kubectl -n luffy get svc eladmin-web
eladmin-web   ClusterIP   10.109.94.95   <none>        80/TCP    2d18h

# 为了更快看到效果，先调整副本数为1
$ kubectl -n luffy scale deploy eladmin-web --replicas=1

# 模拟1000个用户并发访问页面10万次
$ ab -n 100000 -c 1000 http://10.109.94.95:80/

$ kubectl get hpa
$ kubectl -n luffy get pods
```

压力降下来后，会有默认5分钟的`scaledown`的时间，可以通过`controller-manager`的如下参数设置：

```
--horizontal-pod-autoscaler-downscale-stabilization

The value for this option is a duration that specifies how long the autoscaler has to wait before another downscale operation can be performed after the current one has completed. The default value is 5 minutes (5m0s).
```

也可以通过设置每个hpa的`behavior`来控制`scaleDown`和`scaleUp`的行为。

是一个逐步的过程，当前的缩放完成后，下次缩放的时间间隔，比如从3个副本降低到1个副本，中间大概会等待2*5min = 10分钟

###### [基于自定义指标的动态伸缩](http://49.7.203.222:2023/#/kubernetes-advanced/hpa?id=基于自定义指标的动态伸缩)

除了基于 CPU 和内存来进行自动扩缩容之外，我们还可以根据自定义的监控指标来进行。这个我们就需要使用 `Prometheus Adapter`，Prometheus 用于监控应用的负载和集群本身的各种指标，`Prometheus Adapter` 可以帮我们使用 Prometheus 收集的指标并使用它们来制定扩展策略，这些指标都是通过 APIServer 暴露的，而且 HPA 资源对象也可以很轻易的直接使用。

![img](4Kubernetes进阶实践.assets/custom-hpa.webp)

架构图：

![img](4Kubernetes进阶实践.assets/hpa-prometheus-custom.png)

##### [实现原理篇](http://49.7.203.222:2023/#/kubernetes-advanced/hpa?id=实现原理篇)

###### [如何获取Pod的监控数据](http://49.7.203.222:2023/#/kubernetes-advanced/hpa?id=如何获取pod的监控数据)

- k8s 1.8以下：使用heapster，1.11版本完全废弃
- k8s 1.8以上：使用metric-server

官方从 1.8 版本开始提出了 Metric api 的概念，而 metrics-server 就是这种概念下官方的一种实现，用于从 kubelet获取指标，替换掉之前的 heapster。

`Metrics Server` 可以通过标准的 Kubernetes API 把监控数据暴露出来，比如获取某一Pod的监控数据：

```bash
https://172.21.65.226:6443/apis/metrics.k8s.io/v1beta1/namespaces/<namespace-name>/pods/<pod-name>

# https://172.21.65.226:6443/api/v1/namespaces/luffy/pods?limit=500
```

集群中安装了`metrics-server`就可以用上述接口获取Pod的基础监控数据了，如：

```bash
# 获取eladmin-api的pod的监控数据
$ kubectl -n luffy get pod
eladmin-api-6b5d9664d8-gj87w   1/1     Running   0          5d19h

# 则请求的接口应该是 
https://172.21.65.226:6443/apis/metrics.k8s.io/v2/namespaces/luffy/pods/eladmin-api-6b5d9664d8-gj87w

# 我们知道调用apiserver需要认证和鉴权流程，因此，前篇我们已经在luffy名称空间下创建了名为luffy-pods-admin的serviceaccount，并赋予了luffy名称空间的pods的操作权限，因此可以使用该serviceaccount的token来进行认证
$ kubectl -n luffy create token luffy-pods-admin
eyJhbGciOiJSUzI1NiIsImtpZCI6IktJeWtHUFlydXZ2ZncxQVNxUlZyWHhCTkkwb01IbjNKUnFwZ18wUUxkVGcifQ.eyJhdWQiOlsiaHR0cHM6Ly9rdWJlcm5ldGVzLmRlZmF1bHQuc3ZjLmNsdXN0ZXIubG9jYWwiXSwiZXhwIjoxNjY4MjI4Mzg5LCJpYXQiOjE2NjgyMjQ3ODksImlzcyI6Imh0dHBzOi8va3ViZXJuZXRlcy5kZWZhdWx0LnN2Yy5jbHVzdGVyLmxvY2FsIiwia3ViZXJuZXRlcy5pbyI6eyJuYW1lc3BhY2UiOiJsdWZmeSIsInNlcnZpY2VhY2NvdW50Ijp7Im5hbWUiOiJsdWZmeS1wb2RzLWFkbWluIiwidWlkIjoiNjAzYWEzMDYtNDljZi00Y2UxLWI1OGYtMGNmMjUzYTI4YmY2In19LCJuYmYiOjE2NjgyMjQ3ODksInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDpsdWZmeTpsdWZmeS1wb2RzLWFkbWluIn0.HywSHWpsq9yHraUsPwehpaJKWWZFIQY2xE3mZBcVbbXA6ZerEjBzy1q_7VwonNMyUDo_kgK_vM0CVWKDFbESXqG-tbYd6LLD_PNvL8WyEZsKfiK2LYBiTNOAXnUqReUNt9XD_oHVoaEfeEpIO1WPONnmdcOLl_OBa7sdWFH8iT42hVufOHjYELJrOF8PG741BvtMuAIohYwFgO76G8dTWEaOYCX9Rg8n9jJQTqhMvm1fvW6c0V558q63e3oi7OFFR_V90dg4PYbBMAVMrKrrGAogEPnBhHFiY8YKF9lECzTyoVIxOphyvS5M9noU6G_W3-0w7gsMYGrXQVw7xlywNg

$ curl -k  -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IktJeWtHUFlydXZ2ZncxQVNxUlZyWHhCTkkwb01IbjNKUnFwZ18wUUxkVGcifQ.eyJhdWQiOlsiaHR0cHM6Ly9rdWJlcm5ldGVzLmRlZmF1bHQuc3ZjLmNsdXN0ZXIubG9jYWwiXSwiZXhwIjoxNjY4MjI4Mzg5LCJpYXQiOjE2NjgyMjQ3ODksImlzcyI6Imh0dHBzOi8va3ViZXJuZXRlcy5kZWZhdWx0LnN2Yy5jbHVzdGVyLmxvY2FsIiwia3ViZXJuZXRlcy5pbyI6eyJuYW1lc3BhY2UiOiJsdWZmeSIsInNlcnZpY2VhY2NvdW50Ijp7Im5hbWUiOiJsdWZmeS1wb2RzLWFkbWluIiwidWlkIjoiNjAzYWEzMDYtNDljZi00Y2UxLWI1OGYtMGNmMjUzYTI4YmY2In19LCJuYmYiOjE2NjgyMjQ3ODksInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDpsdWZmeTpsdWZmeS1wb2RzLWFkbWluIn0.HywSHWpsq9yHraUsPwehpaJKWWZFIQY2xE3mZBcVbbXA6ZerEjBzy1q_7VwonNMyUDo_kgK_vM0CVWKDFbESXqG-tbYd6LLD_PNvL8WyEZsKfiK2LYBiTNOAXnUqReUNt9XD_oHVoaEfeEpIO1WPONnmdcOLl_OBa7sdWFH8iT42hVufOHjYELJrOF8PG741BvtMuAIohYwFgO76G8dTWEaOYCX9Rg8n9jJQTqhMvm1fvW6c0V558q63e3oi7OFFR_V90dg4PYbBMAVMrKrrGAogEPnBhHFiY8YKF9lECzTyoVIxOphyvS5M9noU6G_W3-0w7gsMYGrXQVw7xlywNg" https://172.21.65.226:6443/apis/metrics.k8s.io/v1beta1/namespaces/luffy/pods/eladmin-api-6b5d9664d8-gj87w
{
  "kind": "PodMetrics",
  "apiVersion": "metrics.k8s.io/v1beta1",
  "metadata": {
    "name": "eladmin-api-6b5d9664d8-gj87w",
    "namespace": "luffy",
    "creationTimestamp": "2022-11-12T03:47:03Z",
    "labels": {
      "app": "eladmin-api",
      "pod-template-hash": "6b5d9664d8"
    }
  },
  "timestamp": "2022-11-12T03:46:47Z",
  "window": "19.07s",
  "containers": [
    {
      "name": "eladmin-api",
      "usage": {
        "cpu": "2082398n",
        "memory": "3795872Ki"
      }
    }
  ]
}
```

目前的采集流程：

![img](4Kubernetes进阶实践.assets/k8s-hpa-ms.png)

###### [kubelet的指标采集](http://49.7.203.222:2023/#/kubernetes-advanced/hpa?id=kubelet的指标采集)

无论是 heapster还是 metric-server，都只是数据的中转和聚合，两者都是调用的 kubelet 的 api 接口获取的数据，而 kubelet 代码中实际采集指标的是 cadvisor 模块，你可以在 node 节点访问 10250 端口获取监控数据：

- Kubelet Summary metrics: https://127.0.0.1:10250/metrics，暴露 node、pod 汇总数据
- Cadvisor metrics: https://127.0.0.1:10250/metrics/cadvisor，暴露 container 维度数据

调用示例：

```bash
$ kubectl -n kube-system create token metrics-server
eyJhbGciOiJSUzI1NiIsImtpZCI6IktJeWtHUFlydXZ2ZncxQVNxUlZyWHhCTkkwb01IbjNKUnFwZ18wUUxkVGcifQ.eyJhdWQiOlsiaHR0cHM6Ly9rdWJlcm5ldGVzLmRlZmF1bHQuc3ZjLmNsdXN0ZXIubG9jYWwiXSwiZXhwIjoxNjY4MjI4ODY0LCJpYXQiOjE2NjgyMjUyNjQsImlzcyI6Imh0dHBzOi8va3ViZXJuZXRlcy5kZWZhdWx0LnN2Yy5jbHVzdGVyLmxvY2FsIiwia3ViZXJuZXRlcy5pbyI6eyJuYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsInNlcnZpY2VhY2NvdW50Ijp7Im5hbWUiOiJtZXRyaWNzLXNlcnZlciIsInVpZCI6IjE4MDJmNGVkLWFjMDYtNDcwYS04YmExLWM0MDJjODgwMjI2OCJ9fSwibmJmIjoxNjY4MjI1MjY0LCJzdWIiOiJzeXN0ZW06c2VydmljZWFjY291bnQ6a3ViZS1zeXN0ZW06bWV0cmljcy1zZXJ2ZXIifQ.Wz3kRbwoCJr2v_Gh5gG9oTMcZOPAgUPcSCmS-Nv7TB7a0aiYzSAqlH2PIqDt1wsv_bmNlpg2QifuDF1lnd5FmBmPCsY-zJX-uW-MStAQaCjfV8iBDmlThIP20srpmMf-z6JzkAlIF7JTTeuv03AkZg50FVKvu_2Zk-lm9gEwUhWgXns3oSnhTCWFHh2rOwnNq3IwcypTrRGWBEt5e9BQ6HWWMiCkkZ0WfgATXAAzYsmzRMIp2ZXntoqYEJGLEwgqJNLPVFpCdSn_C3Ft_2Mnfex84uSH0SL08fD5KP23SibWcPyOHIsSrsuPqA03JF-XW_JjRQyhOZsadSjvTBSSMQ

$ curl -k  -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IktJeWtHUFlydXZ2ZncxQVNxUlZyWHhCTkkwb01IbjNKUnFwZ18wUUxkVGcifQ.eyJhdWQiOlsiaHR0cHM6Ly9rdWJlcm5ldGVzLmRlZmF1bHQuc3ZjLmNsdXN0ZXIubG9jYWwiXSwiZXhwIjoxNjY4MjI4ODY0LCJpYXQiOjE2NjgyMjUyNjQsImlzcyI6Imh0dHBzOi8va3ViZXJuZXRlcy5kZWZhdWx0LnN2Yy5jbHVzdGVyLmxvY2FsIiwia3ViZXJuZXRlcy5pbyI6eyJuYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsInNlcnZpY2VhY2NvdW50Ijp7Im5hbWUiOiJtZXRyaWNzLXNlcnZlciIsInVpZCI6IjE4MDJmNGVkLWFjMDYtNDcwYS04YmExLWM0MDJjODgwMjI2OCJ9fSwibmJmIjoxNjY4MjI1MjY0LCJzdWIiOiJzeXN0ZW06c2VydmljZWFjY291bnQ6a3ViZS1zeXN0ZW06bWV0cmljcy1zZXJ2ZXIifQ.Wz3kRbwoCJr2v_Gh5gG9oTMcZOPAgUPcSCmS-Nv7TB7a0aiYzSAqlH2PIqDt1wsv_bmNlpg2QifuDF1lnd5FmBmPCsY-zJX-uW-MStAQaCjfV8iBDmlThIP20srpmMf-z6JzkAlIF7JTTeuv03AkZg50FVKvu_2Zk-lm9gEwUhWgXns3oSnhTCWFHh2rOwnNq3IwcypTrRGWBEt5e9BQ6HWWMiCkkZ0WfgATXAAzYsmzRMIp2ZXntoqYEJGLEwgqJNLPVFpCdSn_C3Ft_2Mnfex84uSH0SL08fD5KP23SibWcPyOHIsSrsuPqA03JF-XW_JjRQyhOZsadSjvTBSSMQ" https://localhost:10250/metrics
```

kubelet虽然提供了 metric 接口，但实际监控逻辑由内置的cAdvisor模块负责，早期的时候，cadvisor是单独的组件，从k8s 1.12开始，cadvisor 监听的端口在k8s中被删除，所有监控数据统一由Kubelet的API提供。

cadvisor获取指标时实际调用的是 runc/libcontainer库，而libcontainer是对 cgroup文件 的封装，即 cadvsior也只是个转发者，它的数据来自于cgroup文件。

cgroup文件中的值是监控数据的最终来源

Metrics数据流：

![img](4Kubernetes进阶实践.assets/hap-flow.webp)

*思考：Metrics Server是独立的一个服务，只能服务内部实现自己的api，是如何做到通过标准的kubernetes 的API格式暴露出去的*

[kube-aggregator](https://github.com/kubernetes/kube-aggregator)

###### [kube-aggregator聚合器及Metric-Server的实现](http://49.7.203.222:2023/#/kubernetes-advanced/hpa?id=kube-aggregator聚合器及metric-server的实现)

kube-aggregator是对 apiserver 的api的一种拓展机制，它允许开发人员编写一个自己的服务，并把这个服务注册到k8s的api里面，即扩展 API 。

![img](4Kubernetes进阶实践.assets/kube-aggregation.webp)

看下metric-server的实现：

```bash
$ kubectl get apiservice 
NAME                       SERVICE                      AVAILABLE                      
v1beta1.metrics.k8s.io   kube-system/metrics-server        True

$ kubectl get apiservice v1beta1.metrics.k8s.io -oyaml
...
spec:
  group: metrics.k8s.io
  groupPriorityMinimum: 100
  insecureSkipTLSVerify: true
  service:
    name: metrics-server
    namespace: kube-system
    port: 443
  version: v1beta1
  versionPriority: 100
...

# 会往apiserver里注册一个
# proxyPath := "/apis/" + apiService.Spec.Group + "/" + apiService.Spec.Version
# https://172.21.65.226:6443/apis/metrics.k8s.io/v1beta1 
# => https://metrics-server:443/apis/metrics.k8s.io/v1beta1 

$ kubectl -n kube-system get svc metrics-server
NAME             TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)   AGE
metrics-server   ClusterIP   10.106.62.186   <none>        443/TCP   13h

$ kubectl -n luffy create token luffy-pods-admin
eyJhbGciOiJSUzI1NiIsImtpZCI6IktJeWtHUFlydXZ2ZncxQVNxUlZyWHhCTkkwb01IbjNKUnFwZ18wUUxkVGcifQ.eyJhdWQiOlsiaHR0cHM6Ly9rdWJlcm5ldGVzLmRlZmF1bHQuc3ZjLmNsdXN0ZXIubG9jYWwiXSwiZXhwIjoxNjY4MjI5OTMyLCJpYXQiOjE2NjgyMjYzMzIsImlzcyI6Imh0dHBzOi8va3ViZXJuZXRlcy5kZWZhdWx0LnN2Yy5jbHVzdGVyLmxvY2FsIiwia3ViZXJuZXRlcy5pbyI6eyJuYW1lc3BhY2UiOiJsdWZmeSIsInNlcnZpY2VhY2NvdW50Ijp7Im5hbWUiOiJsdWZmeS1wb2RzLWFkbWluIiwidWlkIjoiNjAzYWEzMDYtNDljZi00Y2UxLWI1OGYtMGNmMjUzYTI4YmY2In19LCJuYmYiOjE2NjgyMjYzMzIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDpsdWZmeTpsdWZmeS1wb2RzLWFkbWluIn0.LeKFaXBeaAsyHd06JFc6exenNtfuBadjUj3YtqgHiBMmhNds4zmB9_ysvI4p04W6Kov37YTZg4WSj_AqpsplfCVVg8h-3kAQfPC6cHG5oBN-VUsMC80lu-MZsBTI4C5in7WgddFyFqFMxXL_-TdpguYohOJ6NC90z3IGLCKy8pS5mOCUA34o1_9x5P3JM5e--R-NIbwZmdESkfHejiaENCau_cwP2L2lxmU364kppSrcX_kGLybT7nMV-Bg6Q_-pt0JZVtP5C5NZUuLN0Mtmsd9me8LJFyPDX4fkWtXwZraqiRDx_OTgbckIwQAIDseFEu8ikVBYZ2p6qPCvtIgsMQ

$ curl -k  -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IktJeWtHUFlydXZ2ZncxQVNxUlZyWHhCTkkwb01IbjNKUnFwZ18wUUxkVGcifQ.eyJhdWQiOlsiaHR0cHM6Ly9rdWJlcm5ldGVzLmRlZmF1bHQuc3ZjLmNsdXN0ZXIubG9jYWwiXSwiZXhwIjoxNjY4MjI5OTMyLCJpYXQiOjE2NjgyMjYzMzIsImlzcyI6Imh0dHBzOi8va3ViZXJuZXRlcy5kZWZhdWx0LnN2Yy5jbHVzdGVyLmxvY2FsIiwia3ViZXJuZXRlcy5pbyI6eyJuYW1lc3BhY2UiOiJsdWZmeSIsInNlcnZpY2VhY2NvdW50Ijp7Im5hbWUiOiJsdWZmeS1wb2RzLWFkbWluIiwidWlkIjoiNjAzYWEzMDYtNDljZi00Y2UxLWI1OGYtMGNmMjUzYTI4YmY2In19LCJuYmYiOjE2NjgyMjYzMzIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDpsdWZmeTpsdWZmeS1wb2RzLWFkbWluIn0.LeKFaXBeaAsyHd06JFc6exenNtfuBadjUj3YtqgHiBMmhNds4zmB9_ysvI4p04W6Kov37YTZg4WSj_AqpsplfCVVg8h-3kAQfPC6cHG5oBN-VUsMC80lu-MZsBTI4C5in7WgddFyFqFMxXL_-TdpguYohOJ6NC90z3IGLCKy8pS5mOCUA34o1_9x5P3JM5e--R-NIbwZmdESkfHejiaENCau_cwP2L2lxmU364kppSrcX_kGLybT7nMV-Bg6Q_-pt0JZVtP5C5NZUuLN0Mtmsd9me8LJFyPDX4fkWtXwZraqiRDx_OTgbckIwQAIDseFEu8ikVBYZ2p6qPCvtIgsMQ" https://10.106.62.186/apis/metrics.k8s.io/v1beta1/namespaces/luffy/pods/eladmin-api-6b5d9664d8-gj87w
{
  "kind": "PodMetrics",
  "apiVersion": "metrics.k8s.io/v1beta1",
  "metadata": {
    "name": "eladmin-api-6b5d9664d8-gj87w",
    "namespace": "luffy",
    "creationTimestamp": "2022-11-12T04:12:27Z",
    "labels": {
      "app": "eladmin-api",
      "pod-template-hash": "6b5d9664d8"
    }
  },
  "timestamp": "2022-11-12T04:12:19Z",
  "window": "15.425s",
  "containers": [
    {
      "name": "eladmin-api",
      "usage": {
        "cpu": "1569859n",
        "memory": "3800032Ki"
      }
    }
  ]
}
```





# 对接外部存储

#### [kubernetes对接分部式存储](http://49.7.203.222:2023/#/kubernetes-advanced/pv?id=kubernetes对接分部式存储)

##### [PV与PVC快速入门](http://49.7.203.222:2023/#/kubernetes-advanced/pv?id=pv与pvc快速入门)

k8s存储的目的就是保证Pod重建后，数据不丢失。简单的数据持久化的下述方式：

- emptyDir

  ```yaml
  apiVersion: v1
  kind: Pod
  metadata:
    name: test-pod
  spec:
    containers:
    - image: k8s.gcr.io/test-webserver
      name: webserver
      volumeMounts:
      - mountPath: /cache
        name: cache-volume
    - image: k8s.gcr.io/test-redis
      name: redis
      volumeMounts:
      - mountPath: /data
        name: cache-volume
  volumes:
    - name: cache-volume
      emptyDir: {}
  ```

  - Pod内的容器共享卷的数据
  - 存在于Pod的生命周期，Pod销毁，数据丢失
  - Pod内的容器自动重建后，数据不会丢失

- hostPath

  ```yaml
  apiVersion: v1
  kind: Pod
  metadata:
    name: test-pod
  spec:
    containers:
    - image: k8s.gcr.io/test-webserver
      name: test-container
      volumeMounts:
      - mountPath: /test-pod
        name: test-volume
    volumes:
    - name: test-volume
      hostPath:
        # directory location on host
        path: /data
        # this field is optional
        type: Directory
  ```

  通常配合nodeSelector使用

- nfs存储

  ```yaml
  ...
    volumes:
    - name: redisdata             #卷名称
      nfs:                        #使用NFS网络存储卷
        server: 192.168.31.241    #NFS服务器地址
        path: /data/redis         #NFS服务器共享的目录
        readOnly: false           #是否为只读
  ...
  ```

volume支持的种类众多（参考 https://kubernetes.io/docs/concepts/storage/volumes/#types-of-volumes ），每种对应不同的存储后端实现，因此为了屏蔽后端存储的细节，同时使得Pod在使用存储的时候更加简洁和规范，k8s引入了两个新的资源类型，PV和PVC。

PersistentVolume（持久化卷），是对底层的存储的一种抽象，它和具体的底层的共享存储技术的实现方式有关，比如 Ceph、GlusterFS、NFS 等，都是通过插件机制完成与共享存储的对接。如使用PV对接NFS存储：

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: nfs-pv
spec:
  capacity: 
    storage: 1Gi
  accessModes:
  - ReadWriteMany
  persistentVolumeReclaimPolicy: Retain
  nfs:
    path: /data/k8s
    server: 172.21.65.226
```

- capacity，存储能力， 目前只支持存储空间的设置， 就是我们这里的 storage=1Gi，不过未来可能会加入 IOPS、吞吐量等指标的配置。
- accessModes，访问模式， 是用来对 PV 进行访问模式的设置，用于描述用户应用对存储资源的访问权限，访问权限包括下面几种方式：
  - ReadWriteOnce（RWO）：读写权限，但是只能被单个节点挂载
  - ReadOnlyMany（ROX）：只读权限，可以被多个节点挂载
  - ReadWriteMany（RWX）：读写权限，可以被多个节点挂载

![img](4Kubernetes进阶实践.assets/pv-access-mode.webp)

- persistentVolumeReclaimPolicy，pv的回收策略, 目前只有 NFS 和 HostPath 两种类型支持回收策略
  - Retain（保留）- 保留数据，需要管理员手工清理数据
  - Recycle（回收）- 清除 PV 中的数据，效果相当于执行 rm -rf /thevolume/*
  - Delete（删除）- 与 PV 相连的后端存储完成 volume 的删除操作，当然这常见于云服务商的存储服务，比如 ASW EBS。

因为PV是直接对接底层存储的，就像集群中的Node可以为Pod提供计算资源（CPU和内存）一样，PV可以为Pod提供存储资源。因此PV不是namespaced的资源，属于集群层面可用的资源。Pod如果想使用该PV，需要通过创建PVC挂载到Pod中。

PVC全写是PersistentVolumeClaim（持久化卷声明），PVC 是用户存储的一种声明，创建完成后，可以和PV实现一对一绑定。对于真正使用存储的用户不需要关心底层的存储实现细节，只需要直接使用 PVC 即可。

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: pvc-nfs
  namespace: default
spec:
  accessModes:
  - ReadWriteMany
  resources:
    requests:
      storage: 1Gi
```

然后Pod中通过如下方式去使用：

```yaml
...
    spec:
      containers:
      - name: nginx
        image: nginx:alpine
        imagePullPolicy: IfNotPresent
        ports:
        - containerPort: 80
          name: web
        volumeMounts:                        #挂载容器中的目录到pvc nfs中的目录
        - name: www
          mountPath: /usr/share/nginx/html
      volumes:
      - name: www
        persistentVolumeClaim:              #指定pvc
          claimName: pvc-nfs
...
```

##### [PV与PVC管理NFS存储卷实践](http://49.7.203.222:2023/#/kubernetes-advanced/pv?id=pv与pvc管理nfs存储卷实践)

###### [环境准备](http://49.7.203.222:2023/#/kubernetes-advanced/pv?id=环境准备)

服务端：172.21.65.227

```bash
$ yum -y install nfs-utils rpcbind

# 共享目录
$ mkdir -p /data/k8s && chmod 755 /data/k8s

$ echo '/data/k8s  *(insecure,rw,sync,no_root_squash)'>>/etc/exports

$ systemctl enable rpcbind && systemctl start rpcbind
$ systemctl enable nfs && systemctl start nfs
```

客户端：k8s集群slave节点

```bash
$ yum -y install nfs-utils rpcbind
$ mkdir /nfsdata
$ mount -t nfs 172.21.65.227:/data/k8s /nfsdata
```

###### [PV与PVC演示](http://49.7.203.222:2023/#/kubernetes-advanced/pv?id=pv与pvc演示)

```bash
# 在nfs-server机器中创建
$ mkdir /data/k8s/nginx

# 把/data/k8s/nginx 目录作为数据卷给k8s集群中的Pod使用
$ cat pv-nfs.yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: nfs-pv
spec:
  capacity: 
    storage: 1Gi
  accessModes:
  - ReadWriteMany
  persistentVolumeReclaimPolicy: Retain
  nfs:
    path: /data/k8s/nginx
    server: 172.21.65.227

$ kubectl create -f pv-nfs.yaml

$ kubectl get pv
NAME     CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS      CLAIM   STORAGECLASS  
nfs-pv   1Gi        RWO            Retain           Available
```

一个 PV 的生命周期中，可能会处于4中不同的阶段：

- Available（可用）：表示可用状态，还未被任何 PVC 绑定
- Bound（已绑定）：表示 PV 已经被 PVC 绑定
- Released（已释放）：PVC 被删除，但是资源还未被集群重新声明
- Failed（失败）： 表示该 PV 的自动回收失败

```bash
$ cat pvc.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: pvc-nfs
  namespace: default
spec:
  accessModes:
  - ReadWriteMany
  resources:
    requests:
      storage: 1Gi

$ kubectl create -f pvc.yaml
$ kubectl get pvc
NAME      STATUS   VOLUME   CAPACITY   ACCESS MODES   STORAGECLASS   AGE
pvc-nfs   Bound    nfs-pv   1Gi        RWO                           3s
$ kubectl get pv
NAME     CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM             
nfs-pv   1Gi        RWO            Retain           Bound    default/pvc-nfs             

#访问模式，storage大小（pvc大小需要小于pv大小），以及 PV 和 PVC 的 storageClassName 字段必须一样，这样才能够进行绑定。

#PersistentVolumeController会不断地循环去查看每一个 PVC，是不是已经处于 Bound（已绑定）状态。如果不是，那它就会遍历所有的、可用的 PV，并尝试将其与未绑定的 PVC 进行绑定，这样，Kubernetes 就可以保证用户提交的每一个 PVC，只要有合适的 PV 出现，它就能够很快进入绑定状态。而所谓将一个 PV 与 PVC 进行“绑定”，其实就是将这个 PV 对象的名字，填在了 PVC 对象的 spec.volumeName 字段上。

# 查看nfs数据目录
$ ls /nfsdata
```

创建Pod挂载pvc

```bash
$ cat deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nfs-pvc
spec:
  replicas: 1
  selector:        #指定Pod的选择器
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:alpine
        imagePullPolicy: IfNotPresent
        ports:
        - containerPort: 80
          name: web
        volumeMounts:                        #挂载容器中的目录到pvc nfs中的目录
        - name: www
          mountPath: /usr/share/nginx/html
      volumes:
      - name: www
        persistentVolumeClaim:              #指定pvc
          claimName: pvc-nfs
          
          
$ kubectl create -f deployment.yaml

# 查看容器/usr/share/nginx/html目录

# 删除pvc
```

###### [storageClass实现动态挂载](http://49.7.203.222:2023/#/kubernetes-advanced/pv?id=storageclass实现动态挂载)

创建pv及pvc过程是手动，且pv与pvc一一对应，手动创建很繁琐。因此，通过storageClass + provisioner的方式来实现通过PVC自动创建并绑定PV。

![img](4Kubernetes进阶实践.assets/storage-class.png)

部署： https://github.com/kubernetes-retired/external-storage

*provisioner.yaml*

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nfs-client-provisioner
  labels:
    app: nfs-client-provisioner
  # replace with namespace where provisioner is deployed
  namespace: nfs-provisioner
spec:
  replicas: 1
  selector:
    matchLabels:
      app: nfs-client-provisioner
  strategy:
    type: Recreate
  selector:
    matchLabels:
      app: nfs-client-provisioner
  template:
    metadata:
      labels:
        app: nfs-client-provisioner
    spec:
      serviceAccountName: nfs-client-provisioner
      containers:
        - name: nfs-client-provisioner
          image: registry.cn-beijing.aliyuncs.com/mydlq/nfs-subdir-external-provisioner:v4.0.0
          volumeMounts:
            - name: nfs-client-root
              mountPath: /persistentvolumes
          env:
            - name: PROVISIONER_NAME
              value: luffy.com/nfs
            - name: NFS_SERVER
              value: 172.21.65.227
            - name: NFS_PATH  
              value: /data/k8s
      volumes:
        - name: nfs-client-root
          nfs:
            server: 172.21.65.227
            path: /data/k8s
```

*rbac.yaml*

```yaml
kind: ServiceAccount
apiVersion: v1
metadata:
  name: nfs-client-provisioner
  namespace: nfs-provisioner
---
kind: ClusterRole
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: nfs-client-provisioner-runner
  namespace: nfs-provisioner
rules:
  - apiGroups: [""]
    resources: ["persistentvolumes"]
    verbs: ["get", "list", "watch", "create", "delete"]
  - apiGroups: [""]
    resources: ["persistentvolumeclaims"]
    verbs: ["get", "list", "watch", "update"]
  - apiGroups: ["storage.k8s.io"]
    resources: ["storageclasses"]
    verbs: ["get", "list", "watch"]
  - apiGroups: [""]
    resources: ["events"]
    verbs: ["create", "update", "patch"]
---
kind: ClusterRoleBinding
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: run-nfs-client-provisioner
  namespace: nfs-provisioner
subjects:
  - kind: ServiceAccount
    name: nfs-client-provisioner
    namespace: nfs-provisioner
roleRef:
  kind: ClusterRole
  name: nfs-client-provisioner-runner
  apiGroup: rbac.authorization.k8s.io
---
kind: Role
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: leader-locking-nfs-client-provisioner
  namespace: nfs-provisioner
rules:
  - apiGroups: [""]
    resources: ["endpoints"]
    verbs: ["get", "list", "watch", "create", "update", "patch"]
---
kind: RoleBinding
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: leader-locking-nfs-client-provisioner
  namespace: nfs-provisioner
subjects:
  - kind: ServiceAccount
    name: nfs-client-provisioner
    # replace with namespace where provisioner is deployed
    namespace: nfs-provisioner
roleRef:
  kind: Role
  name: leader-locking-nfs-client-provisioner
  apiGroup: rbac.authorization.k8s.io
```

*storage-class.yaml*

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  annotations:
    storageclass.kubernetes.io/is-default-class: "true"   # 设置为default StorageClass
  name: nfs
provisioner: luffy.com/nfs
parameters:
  archiveOnDelete: "true"
```

创建上述资源：

```bash
$ kubectl create namespace nfs-provisioner
$ kubectl create -f rbac.yaml
$ kubectl create -f provisioner.yaml
$ kubectl create -f storage-class.yaml

# 等待pod启动成功
$ kubectl -n nfs-provisioner get pod 
nfs-client-provisioner-6cfb58c597-rmc45   1/1     Running   0          27s  
```

验证使用`storageclass`自动创建并绑定pv

*pvc.yaml*

```yaml
kind: PersistentVolumeClaim
apiVersion: v1
metadata:
  name: test-claim
spec:
  accessModes:
    - ReadWriteMany
  resources:
    requests:
      storage: 1Mi
  storageClassName: nfs
```

##### [安装容器管理平台](http://49.7.203.222:2023/#/kubernetes-advanced/pv?id=安装容器管理平台)

市面上存在很多开源的容器管理平台，可以帮助用户快速管理k8s平台中的业务服务，今天学习下`kubesphere`的使用。

###### [安装](http://49.7.203.222:2023/#/kubernetes-advanced/pv?id=安装)

安装的版本为`v3.3.1`

- 前置要求

  要求集群中存在默认的`StorageClass`，上篇中我们把nfs设置为了集群默认的存储类，因此满足要求。

  https://kubesphere.com.cn/docs/v3.3/installing-on-kubernetes/introduction/prerequisites/

- 下载初始化安装文件

  ```bash
  wget https://github.com/kubesphere/ks-installer/releases/download/v3.3.1/kubesphere-installer.yaml
  wget https://github.com/kubesphere/ks-installer/releases/download/v3.3.1/cluster-configuration.yaml
  ```

- 安装

  ```bash
  kubectl apply -f kubesphere-installer.yaml
  kubectl apply -f cluster-configuration.yaml
  
  # 查看安装器日志
  kubectl -n kubesphere-system get pod
  ks-installer-746f68548d-fc5tk   1/1     Running   0          2m4s
  
  kubectl -n  kubesphere-system logs -f ks-installer-746f68548d-fc5tk
  ```

- 卸载

  ```bash
  # 如果想卸载kubesphere
  https://github.com/kubesphere/ks-installer/blob/release-3.3/scripts/kubesphere-delete.sh
  ```

##### [对接Ceph存储实践](http://49.7.203.222:2023/#/kubernetes-advanced/pv?id=对接ceph存储实践)

ceph集群的安装及使用参考https://i4t.com/5267.html

单点快速安装： https://blog.csdn.net/h106140873/article/details/90201379

以`k8s-slave2`为例的步骤：

```bash
# 登录k8s-slave2,确保有一块独立磁盘,本例使用/dev/sdb设备
$ fdisk -l

Disk /dev/sda: 85.9 GB, 85899345920 bytes, 167772160 sectors
Units = sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disk label type: dos
Disk identifier: 0x000b2f57

   Device Boot      Start         End      Blocks   Id  System
/dev/sda1   *        2048     4196351     2097152   83  Linux
/dev/sda2         4196352    12584959     4194304   82  Linux swap / Solaris
/dev/sda3        12584960   167772159    77593600   83  Linux

Disk /dev/sdb: 107.4 GB, 107374182400 bytes, 209715200 sectors
Units = sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes

## 执行下述命令
HOSTNAME=k8s-slave2
echo "172.21.65.228 $HOSTNAME" >>/etc/hosts
yum install -y epel-release

cat <<EOF > /etc/yum.repos.d/ceph.repo
[Ceph]
name=Ceph packages for $basearch
baseurl=http://mirrors.163.com/ceph/rpm-jewel/el7/x86_64
enabled=1
gpgcheck=1
type=rpm-md
gpgkey=http://mirrors.163.com/ceph/keys/release.asc
priority=1
[Ceph-noarch]
name=Ceph noarch packages
baseurl=http://mirrors.163.com/ceph/rpm-jewel/el7/noarch
enabled=1
gpgcheck=1
type=rpm-md
gpgkey=http://mirrors.163.com/ceph/keys/release.asc
priority=1
[ceph-source]
name=Ceph source packages
baseurl=http://mirrors.163.com/ceph/rpm-jewel/el7/SRPMS
enabled=1
gpgcheck=1
type=rpm-md
gpgkey=http://mirrors.163.com/ceph/keys/release.asc
priority=1
EOF

# 安装ceph-deploy工具
yum -y install ceph-deploy

# 配置目录并初始化
mkdir /etc/ceph &&cd /etc/ceph
ceph-deploy new $HOSTNAME

# 修改配置文件
cp ceph.conf ceph.conf.bak
sed -i 's@^$@osd_pool_default_size = 1@g' ceph.conf
echo "mon_pg_warn_max_per_osd = 1000" >> /etc/ceph/ceph.conf

# 安装ceph
ceph-deploy install $HOSTNAME

# 创建monitor服务
ceph-deploy mon create $HOSTNAME
ceph-deploy  gatherkeys $HOSTNAME

# 准备osd
mkfs.xfs  /dev/sdb
mkdir -p /var/local/osd
mount /dev/sdb  /var/local/osd/
chown -R ceph:ceph /var/local/osd*

# 创建、激活osd并查看osd
ceph-deploy osd prepare $HOSTNAME:/var/local/osd
ceph-deploy osd activate $HOSTNAME:/var/local/osd
ceph-deploy osd list $HOSTNAME

# 修改配置文件权限
ceph-deploy admin $HOSTNAME
chmod +r /etc/ceph/*

# 部署mds服务
ceph-deploy mds create $HOSTNAME
ceph mds stat

# 创建ceph文件系统
ceph osd pool create cephfs_data 128
ceph osd pool create cephfs_metadata 128
ceph fs new cephfs cephfs_metadata cephfs_data
ceph fs ls

# 查看ceph状态
ceph mon stat
ceph osd stat
ceph -s

# 挂载验证
# ceph auth get-key client.admin
AQCdaG9jP09dJBAAZsl58WHL/xLNvUq7IXh1zQ==

mount -t ceph 172.21.65.228:6789:/ /mnt/cephfs -o name=admin,secret=AQCdaG9jP09dJBAAZsl58WHL/xLNvUq7IXh1zQ==
```

![img](4Kubernetes进阶实践.assets/ceph-art.png)

###### [storageClass实现动态挂载](http://49.7.203.222:2023/#/kubernetes-advanced/pv?id=storageclass实现动态挂载-1)

创建pv及pvc过程是手动，且pv与pvc一一对应，手动创建很繁琐。因此，通过storageClass + provisioner的方式来实现通过PVC自动创建并绑定PV

![img](4Kubernetes进阶实践.assets/storage-class.png)

NFS，ceph-rbd，cephfs均提供了对应的provisioner

部署cephfs-provisioner

```bash
$ cat external-storage-cephfs-provisioner.yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: cephfs-provisioner
  namespace: kube-system
---
kind: ClusterRole
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: cephfs-provisioner
rules:
  - apiGroups: [""]
    resources: ["persistentvolumes"]
    verbs: ["get", "list", "watch", "create", "delete"]
  - apiGroups: [""]
    resources: ["persistentvolumeclaims"]
    verbs: ["get", "list", "watch", "update"]
  - apiGroups: ["storage.k8s.io"]
    resources: ["storageclasses"]
    verbs: ["get", "list", "watch"]
  - apiGroups: [""]
    resources: ["events"]
    verbs: ["create", "update", "patch"]
  - apiGroups: [""]
    resources: ["endpoints"]
    verbs: ["get", "list", "watch", "create", "update", "patch"]
  - apiGroups: [""]
    resources: ["secrets"]
    verbs: ["create", "get", "delete"]
---
kind: ClusterRoleBinding
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: cephfs-provisioner
subjects:
  - kind: ServiceAccount
    name: cephfs-provisioner
    namespace: kube-system
roleRef:
  kind: ClusterRole
  name: cephfs-provisioner
  apiGroup: rbac.authorization.k8s.io


---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: cephfs-provisioner
  namespace: kube-system
spec:
  replicas: 1
  selector:
    matchLabels:
      app: cephfs-provisioner
  strategy:
    type: Recreate
  template:
    metadata:
      labels:
        app: cephfs-provisioner
    spec:
      containers:
      - name: cephfs-provisioner
        image: "quay.io/external_storage/cephfs-provisioner:latest"
        env:
        - name: PROVISIONER_NAME
          value: ceph.com/cephfs
        imagePullPolicy: IfNotPresent
        command:
        - "/usr/local/bin/cephfs-provisioner"
        args:
        - "-id=cephfs-provisioner-1"
        - "-disable-ceph-namespace-isolation=true"
      serviceAccount: cephfs-provisioner
```

在ceph monitor机器中查看admin账户的key

```bash
$ ceph auth get-key client.admin
AQCdaG9jP09dJBAAZsl58WHL/xLNvUq7IXh1zQ==
```

创建secret

```bash
$ echo -n AQCdaG9jP09dJBAAZsl58WHL/xLNvUq7IXh1zQ==|base64
QVFDZGFHOWpQMDlkSkJBQVpzbDU4V0hML3hMTnZVcTdJWGgxelE9PQ==
$ cat ceph-admin-secret.yaml
apiVersion: v1
data:
  key: QVFDZGFHOWpQMDlkSkJBQVpzbDU4V0hML3hMTnZVcTdJWGgxelE9PQ==
kind: Secret
metadata:
  name: ceph-admin-secret
  namespace: kube-system
type: Opaque
```

创建storageclass

```bash
$ cat cephfs-storage-class.yaml
kind: StorageClass
apiVersion: storage.k8s.io/v1
metadata:
  name: dynamic-cephfs
provisioner: ceph.com/cephfs
parameters:
    monitors: 172.21.65.228:6789
    adminId: admin
    adminSecretName: ceph-admin-secret
    adminSecretNamespace: "kube-system"
    claimRoot: /volumes/kubernetes
```

创建上述资源：

```bash
kubectl create -f ceph-admin-secret.yaml
kubectl create -f external-storage-cephfs-provisioner.yaml
kubectl create -f cephfs-storage-class.yaml

# 查看pod状态
kubectl -n kube-system get pod|grep cephfs
```

###### [动态pvc验证及实现分析](http://49.7.203.222:2023/#/kubernetes-advanced/pv?id=动态pvc验证及实现分析)

使用流程： 创建pvc，指定storageclass和存储大小，即可实现动态存储。

创建pvc测试自动生成pv

```bash
$ cat cephfs-pvc-test.yaml
kind: PersistentVolumeClaim
apiVersion: v1
metadata:
  name: cephfs-claim
spec:
  accessModes:     
    - ReadWriteOnce
  storageClassName: dynamic-cephfs
  resources:
    requests:
      storage: 2Gi

$ kubectl create -f cephfs-pvc-test.yaml

$ kubectl get pv
pvc-2abe427e-7568-442d-939f-2c273695c3db   2Gi        RWO            Delete           Bound      default/cephfs-claim   dynamic-cephfs            1s
```

创建Pod使用pvc挂载cephfs数据盘

```bash
$ cat test-pvc-cephfs.yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx-pod
  labels:
    name: nginx-pod
spec:
  containers:
  - name: nginx-pod
    image: nginx:alpine
    ports:
    - name: web
      containerPort: 80
    volumeMounts:
    - name: cephfs
      mountPath: /usr/share/nginx/html
  volumes:
  - name: cephfs
    persistentVolumeClaim:
      claimName: cephfs-claim
      
$ kubectl create -f test-pvc-cephfs.yaml
```

我们所说的容器的持久化，实际上应该理解为宿主机中volume的持久化，因为Pod是支持销毁重建的，所以只能通过宿主机volume持久化，然后挂载到Pod内部来实现Pod的数据持久化。

宿主机上的volume持久化，因为要支持数据漂移，所以通常是数据存储在分布式存储中，宿主机本地挂载远程存储（NFS，Ceph，OSS），这样即使Pod漂移也不影响数据。

k8s的pod的挂载盘通常的格式为：

```bash
/var/lib/kubelet/pods/<Pod的ID>/volumes/kubernetes.io~<Volume类型>/<Volume名字>
```





# 集群网络

#### [Kubernetes集群的网络实现](http://49.7.203.222:2023/#/kubernetes-advanced/cni?id=kubernetes集群的网络实现)

##### [容器网络回顾](http://49.7.203.222:2023/#/kubernetes-advanced/cni?id=容器网络回顾)

![img](4Kubernetes进阶实践.assets/docker-bridge.jpeg)

Docker 创建一个容器的时候，会执行如下操作：

- 创建一对虚拟接口/网卡，也就是veth pair；
- veth pair的一端桥接 到默认的 docker0 或指定网桥上，并具有一个唯一的名字，如 vethxxxxxx；
- veth pair的另一端放到新启动的容器内部，并修改名字作为 eth0，这个网卡/接口只在容器的命名空间可见；
- 从网桥可用地址段中（也就是与该bridge对应的network）获取一个空闲地址分配给容器的 eth0
- 配置容器的默认路由

##### [Pod IP唯一性保障](http://49.7.203.222:2023/#/kubernetes-advanced/cni?id=pod-ip唯一性保障)

Kubernetes网络模型的核心要求之一是每个Pod应该获得自己的IP地址，如何实现？

```bash
$ cat /etc/kubernetes/manifests/kube-controller-manager.yaml
...
- --cluster-cidr=10.244.0.0/16
...

# 为每个节点从cidr中分配一个网段，供该节点分配pod ip
$ kubectl describe node k8s-slave1
```

*思考：谁来配置Pod网络？当Pod调度到 k8s-slave1节点后，网络的配置流程是怎样*

##### [Pod配置网络流程](http://49.7.203.222:2023/#/kubernetes-advanced/cni?id=pod配置网络流程)

CNI：容器网络接口（Container Network Interface）， 主要能力是对接 Kubelet 完成容器网卡的创建，申请和设置 ip 地址，路由设置，网关设置，实现kubernetes集群的Pod网络通信及管理。

CNI的具体实现有很多种：

- 通用类型：flannel、calico、Cilium 等，部署使用简单
- 其他：根据具体的网络环境及网络需求选择，比如
  - 公有云机器，可以选择厂商与网络插件的定制Backend，如AWS、阿里、腾讯针对flannel均有自己的插件，也有AWS ECS CNI
  - 私有云厂商，比如Vmware NSX-T等
  - 网络性能等，MacVlan

> k8s本身不提供cni的实现，因此安装完k8s集群后，需要单独安装网络组件

![img](4Kubernetes进阶实践.assets/kubelet-cni-process.jpg)

1. Pod调度到k8s的节点k8s-slave1中
2. slave1的kubelet调用containerd创建Pod
3. containerd创建Pod沙箱和pod所用的网络空间
4. containerd查找配置目录`/etc/cni/net.d/`，发现`10-flannel.conflist`，使用flannel作为网络插件
5. CNI开始为Pod配置网络
   - flannel启动时候，写入了本机配置文件`/run/flannel/subnet.env`
   - flannel将本机网段等信息传递给bridge插件
     - bridge插件创建cni0网桥
     - 创建veth pair，分别接入到pod网络空间和cni0网桥
     - 调用 本地IPAM CNI 插件，设置pod ip地址并记录已分配地址
   - IPAM CNI 插件 从子网返回容器的IP地址，并将分配的IP本地存储在主机上 `/var/lib/cni/networks/cbr0/`
6. containerd创建pause容器，并配置到新建的网络空间
7. kubelet调用containerd开始拉取业务镜像
8. 启动业务容器并设置namespace和cgroup

上图可以清晰的看到如下重点：

- kubelet、containerd、cni的工作边界和职责
- cni是被containerd进行调用，cni的实现是可以根据不同的网络环境配置的
- 配置Pod网络的过程，实际上是一个网络工具的链式调用

更细致的CNI调用过程：

![img](4Kubernetes进阶实践.assets/cni-network.webp)

- Flannel CNI

  - 使用Flannel作为网络提供程序时，Containered CRI插件使用CNI配置文件`/etc/cni/net.d/10-flannel.conflist`调用Flannel CNI插件
  - Fannel CNI插件与Flanneld结合使用。当Flanneld启动时，它会从apiserver中获取podCIDR和其他与网络相关的详细信息，并将它们存储在文件`/run/flannel/subnet.env`中
  - Flannel CNI插件使用`/run/flannel/subnet.env`中的信息来配置和调用网桥CNI插件。

- Bridge CNI

  首次调用Bridge CNI插件时，它将使用配置文件中指定的`"name": "cni0"`创建一个Linux网桥。然后，它为每个Pod创建veth对-该对的一端在容器的网络名称空间中，另一端连接到主机网络上的linux桥。使用Bridge CNI插件，主机上的所有容器都连接到主机网络上的linux网桥。

  配置完veth对后，Bridge插件将调用主机本地IPAM CNI插件

- host-local IPAM CNI

  Host-local IPAM（IP地址管理）插件从子网返回容器的IP地址，并将分配的IP本地存储在主机上

经过Pod网络配置后，本机的Pod应该是这样的：

![img](4Kubernetes进阶实践.assets/pod-local.png)

思考：

- flannel插件和kube-flannel的Pod什么关系
- 跨主机的Pod间如何实现通信

##### [kube-flannel的作用](http://49.7.203.222:2023/#/kubernetes-advanced/cni?id=kube-flannel的作用)

从Pod的启动进程，看flannel的Pod：

```bash
$ kubectl -n kube-flannel get pod kube-flannel-ds-gdvpx -oyaml

# 1. /opt/bin/flanneld --ip-masq --kube-subnet-mgr --iface=eth0
# 2. cp -f /flannel /opt/cni/bin/flannel
# 3. cp -f /etc/kube-flannel/cni-conf.json /etc/cni/net.d/10-flannel.conflist
```

从进程可以得知：

1. 启动flanneld进程，功能未知
2. 拷贝flannel的网络插件到宿主机中，为containerd调用
3. 考虑flannel的配置文件，当成宿主机的CNI配置，告知containerd使用flannel

##### [跨主机Pod通信](http://49.7.203.222:2023/#/kubernetes-advanced/cni?id=跨主机pod通信)

跨主机间的通信流程：

![img](4Kubernetes进阶实践.assets/pods-network.webp)

flannel的网络有多种后端实现：

- udp
- vxlan
- host-gw
- ...

不特殊指定的话，默认会使用vxlan技术作为Backend，可以通过如下查看：

```bash
$ kubectl -n kube-flannel exec  kube-flannel-ds-amd64-cb7hs cat /etc/kube-flannel/net-conf.json
{
  "Network": "10.244.0.0/16",
  "Backend": {
    "Type": "vxlan"
  }
}
```

使用vxlan作为后端实现时，flanneld进程的作用：

- 启动flannel.1作为VTEP设备，用来封包、解包，实现跨主机通信
- 监听宿主机的Pod CIDR，维护本机路由表

###### [vxlan介绍及点对点通信的实现](http://49.7.203.222:2023/#/kubernetes-advanced/cni?id=vxlan介绍及点对点通信的实现)

VXLAN 全称是虚拟可扩展的局域网（ Virtual eXtensible Local Area Network），它是一种 overlay 技术，通过三层的网络来搭建虚拟的二层网络。

![img](4Kubernetes进阶实践.assets/vxlan.png)

它创建在原来的 IP 网络（三层）上，只要是三层可达（能够通过 IP 互相通信）的网络就能部署 vxlan。在每个端点上都有一个 vtep 负责 vxlan 协议报文的封包和解包，也就是在虚拟报文上封装 vtep 通信的报文头部。物理网络上可以创建多个 vxlan 网络，这些 vxlan 网络可以认为是一个隧道，不同节点的虚拟机能够通过隧道直连。每个 vxlan 网络由唯一的 VNI 标识，不同的 vxlan 可以不相互影响。

- VTEP（VXLAN Tunnel Endpoints）：vxlan 网络的边缘设备，用来进行 vxlan 报文的处理（封包和解包）。vtep 可以是网络设备（比如交换机），也可以是一台机器（比如虚拟化集群中的宿主机）
- VNI（VXLAN Network Identifier）：VNI 是每个 vxlan 的标识，一共有 2^24 = 16,777,216，一般每个 VNI 对应一个租户，也就是说使用 vxlan 搭建的公有云可以理论上可以支撑千万级别的租户

演示：在k8s-slave1和k8s-slave2两台机器间，利用vxlan的点对点能力，实现虚拟二层网络的通信

![img](4Kubernetes进阶实践.assets/vxlan-p2p-1.jpg)

`172.21.65.227`节点：

```bash
# 创建vTEP设备，对端指向172.21.65.228节点，指定VNI及underlay网络使用的网卡
$ ip link add vxlan20 type vxlan id 20 remote 172.21.65.228 dstport 4789 dev eth0

$ ip -d link show vxlan20

# 启动设备
$ ip link set vxlan20 up 

# 设置ip地址
$ ip addr add 10.245.1.3/24 dev vxlan20
```

`172.21.65.228`节点：

```bash
# 创建VTEP设备，对端指向172.21.65.227节点，指定VNI及underlay网络使用的网卡
$ ip link add vxlan20 type vxlan id 20 remote 172.21.65.227 dstport 4789 dev eth0

# 启动设备
$ ip link set vxlan20 up 

# 设置ip地址
$ ip addr add 10.245.2.5/24 dev vxlan20
```

在`172.21.65.227`节点：

```bash
$ ping 10.245.2.5

# 走vtep封包解包

$ ip route add 10.245.2.0/24 dev vxlan20

# 在172.21.65.228机器
$ ip route add 10.245.1.0/24 dev vxlan20

# 再次ping
$ ping 10.245.2.5
```

![img](4Kubernetes进阶实践.assets/vxlan-p2p-2.jpg)

隧道是一个逻辑上的概念，在 vxlan 模型中并没有具体的物理实体相对应。隧道可以看做是一种虚拟通道，vxlan 通信双方（图中的虚拟机）认为自己是在直接通信，并不知道底层网络的存在。从整体来说，每个 vxlan 网络像是为通信的虚拟机搭建了一个单独的通信通道，也就是隧道。

实现的过程：

虚拟机的报文通过 vtep 添加上 vxlan 以及外部的报文层，然后发送出去，对方 vtep 收到之后拆除 vxlan 头部然后根据 VNI 把原始报文发送到目的虚拟机。

```bash
# 查看172.21.65.227主机路由
$ route -n
10.0.51.0       0.0.0.0         255.255.255.0   U     0      0        0 vxlan20
10.0.52.0       0.0.0.0         255.255.255.0   U     0      0        0 vxlan20

# 到了vxlan的设备后，
$ ip -d link show vxlan20
    vxlan id 20 remote 172.21.65.228 dev eth0 srcport 0 0 dstport 4789 ...
```

清理：

```bash
$ ip link del vxlan20
```

演示跨主机Pod通信的流量详细过程：

```bash
$ kubectl -n luffy get po -o wide
eladmin-api-6b5d9664d8-gj87w   1/1     Running   1    11d     10.244.1.35   k8s-slave1
eladmin-web-6c5dc87987-ncm5d   1/1     Running   0    4d23h   10.244.0.21   k8s-master

$ kubectl -n luffy exec eladmin-web-6c5dc87987-ncm5d  -- ping 10.244.1.35 -c 2
PING 10.244.1.35 (10.244.1.35): 56 data bytes
64 bytes from 10.244.1.35: seq=0 ttl=62 time=0.473 ms
64 bytes from 10.244.1.35: seq=1 ttl=62 time=0.413 ms

--- 10.244.1.35 ping statistics ---
2 packets transmitted, 2 packets received, 0% packet loss
round-trip min/avg/max = 0.413/0.443/0.473 ms

# 查看路由
$ kubectl -n luffy eladmin-web-6c5dc87987-ncm5d -- route -n
Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
0.0.0.0         10.244.0.1      0.0.0.0         UG    0      0        0 eth0
10.244.0.0      0.0.0.0         255.255.255.0   U     0      0        0 eth0
10.244.0.0      10.244.0.1      255.255.0.0     UG    0      0        0 eth0

# 查看k8s-master 的veth pair 和网桥
$ brctl show
bridge name     bridge id               STP enabled     interfaces
cni0            8000.6a9a0b341d88       no              veth048cc253
                                                        veth76f8e4ce
                                                        vetha4c972e1
# 流量到了cni0后，查看master节点的route
$ route -n
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
0.0.0.0         192.168.136.2   0.0.0.0         UG    100    0        0 eth0
10.0.136.0      0.0.0.0         255.255.255.0   U     0      0        0 vxlan20
10.244.0.0      10.244.0.0      255.255.255.0   UG    0      0        0 flannel.1
10.244.1.0      0.0.0.0         255.255.255.0   U     0      0        0 cni0
10.244.2.0      10.244.2.0      255.255.255.0   UG    0      0        0 flannel.1
172.17.0.0      0.0.0.0         255.255.0.0     U     0      0        0 docker0
192.168.136.0   0.0.0.0         255.255.255.0   U     100    0        0 eth0

# 流量转发到了flannel.1网卡，查看该网卡，其实是vtep设备
$ ip -d link show flannel.1
602: flannel.1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1450 qdisc noqueue state UNKNOWN mode DEFAULT group default
    link/ether 1a:ef:13:b7:44:9c brd ff:ff:ff:ff:ff:ff promiscuity 0
    vxlan id 1 local 172.21.65.226 dev eth0 srcport 0 0 dstport 8472 nolearning ageing 300 noudpcsum noudp6zerocsumtx noudp6zerocsumrx addrgenmode eui64 numtxqueues 1 numrxqueues 1 gso_max_size 65536 gso_max_segs 65535

# 该转发到哪里，通过etcd查询数据，然后本地缓存，流量不用走多播发送
$ bridge fdb show dev flannel.1
4a:4d:9d:3a:c5:f0 dst 172.21.51.68 self permanent
76:e7:98:9f:5b:e9 dst 172.21.51.67 self permanent

# 对端的vtep设备接收到请求后做解包，取出源payload内容，查看k8s-slave1的路由
$ route -n
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
0.0.0.0         172.21.64.190   0.0.0.0         UG    0      0        0 eth0
10.244.0.0      10.244.0.0      255.255.255.0   UG    0      0        0 flannel.1
10.244.1.0      0.0.0.0         255.255.255.0   U     0      0        0 cni0
10.244.2.0      10.244.2.0      255.255.255.0   UG    0      0        0 flannel.1
169.254.0.0     0.0.0.0         255.255.0.0     U     1002   0        0 eth0
172.17.0.0      0.0.0.0         255.255.0.0     U     0      0        0 docker0

#根据路由规则转发到cni0网桥,然后由网桥转到具体的Pod中
```

实际的请求图：

![img](4Kubernetes进阶实践.assets/flannel-actual.png)

###### [利用host-gw模式提升集群网络性能](http://49.7.203.222:2023/#/kubernetes-advanced/cni?id=利用host-gw模式提升集群网络性能)

vxlan模式适用于三层可达的网络环境，对集群的网络要求很宽松，但是同时由于会通过VTEP设备进行额外封包和解包，因此给性能带来了额外的开销。

网络插件的目的其实就是将本机的cni0网桥的流量送到目的主机的cni0网桥。实际上有很多集群是部署在同一二层网络环境下的，可以直接利用二层的主机当作流量转发的网关。这样的话，可以不用进行封包解包，直接通过路由表去转发流量。

![img](4Kubernetes进阶实践.assets/flannel-host-gw.png)

为什么三层可达的网络不直接利用网关转发流量？

```bash
内核当中的路由规则，网关必须在跟主机当中至少一个 IP 处于同一网段。
由于k8s集群内部各节点均需要实现Pod互通，因此，也就意味着host-gw模式需要整个集群节点都在同一二层网络内。
```

修改flannel的网络后端：

```bash
$ kubectl edit cm kube-flannel-cfg -n kube-flannel
...
net-conf.json: |
    {
      "Network": "10.244.0.0/16",
      "Backend": {
        "Type": "host-gw"
      }
    }
kind: ConfigMap
...
```

重建Flannel的Pod

```bash
$ kubectl -n kube-flannel get pod
kube-flannel-ds-amd64-5dgb8          1/1     Running   0          15m
kube-flannel-ds-amd64-c2gdc          1/1     Running   0          14m
kube-flannel-ds-amd64-t2jdd          1/1     Running   0          15m

$ kubectl -n kube-flannel delete po kube-flannel-ds-amd64-5dgb8 kube-flannel-ds-amd64-c2gdc kube-flannel-ds-amd64-t2jdd

# 等待Pod新启动后，查看日志，出现Backend type: host-gw字样
$  kubectl -n kube-system logs -f kube-flannel-ds-amd64-4hjdw
I0704 01:18:11.916374       1 kube.go:126] Waiting 10m0s for node controller to sync
I0704 01:18:11.916579       1 kube.go:309] Starting kube subnet manager
I0704 01:18:12.917339       1 kube.go:133] Node controller sync successful
I0704 01:18:12.917848       1 main.go:247] Installing signal handlers
I0704 01:18:12.918569       1 main.go:386] Found network config - Backend type: host-gw
I0704 01:18:13.017841       1 main.go:317] Wrote subnet file to /run/flannel/subnet.env
```

查看节点路由表：

```bash
$ route -n 
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
0.0.0.0         172.21.64.190   0.0.0.0         UG    0      0        0 eth0
10.244.0.0      0.0.0.0         255.255.255.0   U     0      0        0 cni0
10.244.1.0      172.21.65.227   255.255.255.0   UG    0      0        0 eth0
10.244.2.0      172.21.65.228   255.255.255.0   UG    0      0        0 eth0
169.254.0.0     0.0.0.0         255.255.0.0     U     1002   0        0 eth0
172.17.0.0      0.0.0.0         255.255.0.0     U     0      0        0 docker0
```

##### [总结](http://49.7.203.222:2023/#/kubernetes-advanced/cni?id=总结)

flannel pod做的几个事情：

- 为了配置本机的Pod网络
  - flannel pod启动时，拷贝cni的配置文件`/etc/cni/net.d/10-flannel.conflist`，告知CRI(containerd) 使用flannel插件进行配置网络
  - 拷贝一份可执行文件到宿主机 `/opt/cni/bin/flannel`
  - 调用apiserver，得到分配到本机的PodCIDR，写入到`/run/flannel/subnet.env`
  - 调用本机的bridge插件，创建本地cni0网桥，创建虚拟网卡对，链接cni0和Pod网络空间
  - bridge cni调用local ipam插件（host-local），记录并分配pod ip，写入到`/var/lib/cni/networks/cbr0/`
- 为了使得跨主机实现Pod的访问
  - 创建flannel.1 vtep设备，支持vxlan模式下封包解包
  - 维护本机路由表，转发Pod的流量



# Helm部署应用

#### [使用Helm3管理复杂应用的部署](http://49.7.203.222:2023/#/kubernetes-advanced/helm?id=使用helm3管理复杂应用的部署)

##### [认识Helm](http://49.7.203.222:2023/#/kubernetes-advanced/helm?id=认识helm)

1. Helm的重要概念
   - chart，应用的信息集合，包括各种对象的配置模板、参数定义、依赖关系、文档说明等
   - Repoistory，chart仓库，存储chart的地方，并且提供了一个该 Repository 的 Chart 包的清单文件以供查询。Helm 可以同时管理多个不同的 Repository。
   - release， 当 chart 被安装到 kubernetes 集群，就生成了一个 release ， 是 chart 的运行实例，代表了一个正在运行的应用

helm 是包管理工具，包就是指 chart，helm 能够：

- 从零创建chart
- 与仓库交互，拉取、保存、更新 chart
- 在kubernetes集群中安装、卸载 release
- 更新、回滚、测试 release

##### [安装与快速入门实践](http://49.7.203.222:2023/#/kubernetes-advanced/helm?id=安装与快速入门实践)

下载最新的稳定版本：https://get.helm.sh/helm-v3.2.4-linux-amd64.tar.gz

或者：链接: https://pan.baidu.com/s/1zE9KE8p_RbreZoKx0gA3cg 提取码: hmfm

```bash
# k8s-master节点
$ wget https://get.helm.sh/helm-v3.2.4-linux-amd64.tar.gz
$ tar -zxf helm-v3.2.4-linux-amd64.tar.gz

$ cp linux-amd64/helm /usr/sbin/

# 验证安装
$ helm version
version.BuildInfo{Version:"v3.2.4", GitCommit:"0ad800ef43d3b826f31a5ad8dfbb4fe05d143688", GitTreeState:"clean", GoVersion:"go1.13.12"}
$ helm env

# 查看仓库
$ helm repo ls
# 添加仓库
$ helm repo add stable https://charts.bitnami.com/bitnami
# 同步最新charts信息到本地
$ helm repo update
```

快速入门实践：

示例一：使用helm安装wordpress应用

```bash
# helm 搜索chart包
$ helm search repo wordpress

$ kubectl create namespace wordpress
# 从仓库安装
$ helm -n wordpress install wordpress stable/wordpress --set mariadb.primary.persistence.enabled=false --set service.type=ClusterIP --set ingress.enabled=true --set persistence.enabled=false --set ingress.hostname=wordpress.luffy.com

# 查看release
$ helm -n wordpress ls
$ kubectl -n wordpress get all 

# chart不适配k8s的ingress，需要添加上ingressClassName: nginx
$ kubectl -n wordpress edit ing wordpress
...
spec:
  ingressClassName: nginx
  rules:
  - host: wordpress.luffy.com
...

# 从chart仓库中把chart包下载到本地
$ helm pull stable/wordpress


# 卸载
$ helm -n wordpress uninstall wordpress
```

示例二：新建nginx的chart并安装

```bash
$ helm create nginx

# 从本地 安装到别的命名空间demo
$ kubectl create namespace demo
$ helm -n demo install nginx ./nginx --set replicaCount=2 --set image.tag=alpine

# 查看
$ helm ls
$ helm -n demo ls

#
$ kubectl -n demo get all
```

##### [Chart的模板语法及开发](http://49.7.203.222:2023/#/kubernetes-advanced/helm?id=chart的模板语法及开发)

###### [nginx的chart实现分析](http://49.7.203.222:2023/#/kubernetes-advanced/helm?id=nginx的chart实现分析)

格式：

```bash
$ tree nginx/
nginx/
├── charts                        # 存放子chart
├── Chart.yaml                    # 该chart的全局定义信息
├── templates                    # chart运行所需的资源清单模板，用于和values做渲染
│   ├── deployment.yaml
│   ├── _helpers.tpl            # 定义全局的命名模板，方便在其他模板中引入使用
│   ├── hpa.yaml
│   ├── ingress.yaml
│   ├── NOTES.txt                # helm安装完成后终端的提示信息
│   ├── serviceaccount.yaml
│   ├── service.yaml
│   └── tests
│       └── test-connection.yaml
└── values.yaml                    # 模板使用的默认值信息
```

很明显，资源清单都在templates中，数据来源于values.yaml，安装的过程就是将模板与数据融合成k8s可识别的资源清单，然后部署到k8s环境中。

```bash
$ helm install debug-nginx ./nginx --dry-run --set replicaCount=2 --debug
```

分析模板文件的实现：

- 引用命名模板并传递作用域

  ```go
  {{ include "nginx.fullname" . }}
  ```

  include从_helpers.tpl中引用命名模板，并传递顶级作用域.

- 内置对象

  ```go
  .Values
  .Release.Name
  .Chart
  ```

  - ```
    Release
    ```

    ：该对象描述了 release 本身的相关信息，它内部有几个对象：

    - `Release.Name`：release 名称
    - `Release.Namespace`：release 安装到的命名空间
    - `Release.IsUpgrade`：如果当前操作是升级或回滚，则该值为 true
    - `Release.IsInstall`：如果当前操作是安装，则将其设置为 true
    - `Release.Revision`：release 的 revision 版本号，在安装的时候，值为1，每次升级或回滚都会增加
    - `Release.Service`：渲染当前模板的服务，在 Helm 上，实际上该值始终为 Helm

  - `Values`：从 `values.yaml` 文件和用户提供的 values 文件传递到模板的 Values 值

  - `Chart`：获取 `Chart.yaml` 文件的内容，该文件中的任何数据都可以访问，例如 `{{ .Chart.Name }}-{{ .Chart.Version}}` 可以渲染成 `mychart-0.1.0`

- 模板定义

  ```go
  {{- define "nginx.fullname" -}}
  {{- if .Values.fullnameOverride }}
  {{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
  {{- else }}
  {{- $name := default .Chart.Name .Values.nameOverride }}
  {{- if contains $name .Release.Name }}
  {{- .Release.Name | trunc 63 | trimSuffix "-" }}
  {{- else }}
  {{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
  {{- end }}
  {{- end }}
  {{- end }}
  ```

  - {{- 去掉左边的空格及换行，-}} 去掉右侧的空格及换行

  - 示例

    ```yaml
    apiVersion: v1
    kind: ConfigMap
    metadata:
      name: {{ .Release.Name }}-configmap
    data:
      myvalue: "Hello World"
      drink: {{ .Values.favorite.drink | default "tea" | quote }}
      food: {{ .Values.favorite.food | upper | quote }}
      {{ if eq .Values.favorite.drink "coffee" }}
      mug: true
      {{ end }}
    ```

    渲染完后是：

    ```yaml
    apiVersion: v1
    kind: ConfigMap
    metadata:
      name: mychart-1575971172-configmap
    data:
      myvalue: "Hello World"
      drink: "coffee"
      food: "PIZZA"
    
      mug: true
    ```

- 管道及方法

  - trunc表示字符串截取，63作为参数传递给trunc方法，trimSuffix表示去掉`-`后缀

    ```go
    {{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
    ```

  - nindent表示前面的空格数

    ```go
      selector:
        matchLabels:
          {{- include "nginx.selectorLabels" . | nindent 6 }}
    ```

  - lower表示将内容小写，quote表示用双引号引起来

    ```go
    value: {{ include "mytpl" . | lower | quote }}
    ```

- 条件判断语句每个if对应一个end

  ```go
  {{- if .Values.fullnameOverride }}
  ...
  {{- else }}
  ...
  {{- end }}
  ```

  通常用来根据values.yaml中定义的开关来控制模板中的显示：

  ```go
  {{- if not .Values.autoscaling.enabled }}
    replicas: {{ .Values.replicaCount }}
  {{- end }}
  ```

- 定义变量，模板中可以通过变量名字去引用

  ```go
  {{- $name := default .Chart.Name .Values.nameOverride }}
  ```

- 遍历values的数据

  ```go
        {{- with .Values.nodeSelector }}
        nodeSelector:
          {{- toYaml . | nindent 8 }}
        {{- end }}
  ```

  toYaml处理值中的转义及特殊字符， "kubernetes.io/role"=master ， name="value1,value2" 类似的情况

- default设置默认值

  ```go
  image: "{{ .Values.image.repository }}:{{ .Values.image.tag | default .Chart.AppVersion }}"
  ```

Helm template

hpa.yaml

```yaml
{{- if .Values.autoscaling.enabled }}
apiVersion: autoscaling/v2beta1
kind: HorizontalPodAutoscaler
metadata:
  name: {{ include "nginx.fullname" . }}
  labels:
    {{- include "nginx.labels" . | nindent 4 }}
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: {{ include "nginx.fullname" . }}
  minReplicas: {{ .Values.autoscaling.minReplicas }}
  maxReplicas: {{ .Values.autoscaling.maxReplicas }}
  metrics:
  {{- if .Values.autoscaling.targetCPUUtilizationPercentage }}
    - type: Resource
      resource:
        name: cpu
        targetAverageUtilization: {{ .Values.autoscaling.targetCPUUtilizationPercentage }}
  {{- end }}
  {{- if .Values.autoscaling.targetMemoryUtilizationPercentage }}
    - type: Resource
      resource:
        name: memory
        targetAverageUtilization: {{ .Values.autoscaling.targetMemoryUtilizationPercentage }}
  {{- end }}
{{- end }}
```

###### [创建Release的时候赋值](http://49.7.203.222:2023/#/kubernetes-advanced/helm?id=创建release的时候赋值)

- set的方式

```bash
# 改变副本数和resource值
$ helm install nginx-2 ./nginx --set replicaCount=2 --set resources.limits.cpu=200m --set resources.limits.memory=256Mi
```

- value文件的方式

  ```bash
  $ cat nginx-values.yaml
  resources:
    limits:
      cpu: 100m
      memory: 128Mi
    requests:
      cpu: 100m
      memory: 128Mi
  autoscaling:
    enabled: true
    minReplicas: 1
    maxReplicas: 3
    targetCPUUtilizationPercentage: 80
  ingress:
    enabled: true
    hosts:
      - host: chart-example.luffy.com
        paths:
        - /
  
  $ helm install -f nginx-values.yaml nginx-3 ./nginx
  ```

使用helm template查看渲染模板

```bash
$ helm -n luffy template nginx ./nginx --set replicaCount=2 --set image.tag=alpine --set autoscaling.enabled=true
```

更多语法参考：

https://helm.sh/docs/topics/charts/

##### [实战：使用Helm部署Harbor镜像及chart仓库](http://49.7.203.222:2023/#/kubernetes-advanced/helm?id=实战：使用helm部署harbor镜像及chart仓库)

###### [harbor部署](http://49.7.203.222:2023/#/kubernetes-advanced/helm?id=harbor部署)

架构 https://github.com/goharbor/harbor/wiki/Architecture-Overview-of-Harbor

![img](4Kubernetes进阶实践.assets/harbor-architecture.png)

- Core，核心组件
  - API Server，接收处理用户请求
  - Config Manager ：所有系统的配置，比如认证、邮件、证书配置等
  - Project Manager：项目管理
  - Quota Manager ：配额管理
  - Chart Controller：chart管理
  - Replication Controller ：镜像副本控制器，可以与不同类型的仓库实现镜像同步
    - Distribution (docker registry)
    - Docker Hub
    - ...
  - Scan Manager ：扫描管理，引入第三方组件，进行镜像安全扫描
  - Registry Driver ：镜像仓库驱动，目前使用docker registry
- Job Service，执行异步任务，如同步镜像信息
- Log Collector，统一日志收集器，收集各模块日志
- GC Controller
- Chart Museum，chart仓库服务，第三方
- Docker Registry，镜像仓库服务
- kv-storage，redis缓存服务，job service使用，存储job metadata
- local/remote storage，存储服务，比较镜像存储
- SQL Database，postgresl，存储用户、项目等元数据

通常用作企业级镜像仓库服务，实际功能强大很多。

组件众多，因此使用helm部署

```bash
# 添加harbor chart仓库
$ helm repo add harbor https://helm.goharbor.io

# 搜索harbor的chart
$ helm search repo harbor

# 不知道如何部署，因此拉到本地
$ helm pull harbor/harbor
```

创建pvc

```bash
$ kubectl create namespace harbor
$ cat harbor-pvc.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: harbor-data
  namespace: harbor
spec:
  accessModes:
  - ReadWriteMany
  resources:
    requests:
      storage: 20Gi
  storageClassName: nfs

# 创建pvc
kubectl create -f harbor-pvc.yaml
```

修改harbor配置：

- ingress访问的配置（36行和46行）

  ```yaml
   34   ingress:
   35     hosts:
   36       core: core.harbor.domain
   37       notary: notary.harbor.domain
   38     # set to the type of ingress controller if it has specific requirements.
   39     # leave as `default` for most ingress controllers.
   40     # set to `gce` if using the GCE ingress controller
   41     # set to `ncp` if using the NCP (NSX-T Container Plugin) ingress controller
   42     # set to `alb` if using the ALB ingress controller
   43     controller: default
   44     ## Allow .Capabilities.KubeVersion.Version to be overridden while creating ingress
   45     kubeVersionOverride: ""
   46     className: "nginx"
  ```

- externalURL，web访问入口，和ingress的域名相同（126行）

  ```yaml
  126 externalURL: https://harbor.luffy.com
  ```

- 持久化，使用PVC对接的nfs（215，220，225，227，249，251，258，260）

  ```yaml
  204 persistence:
  205   enabled: true
  206   # Setting it to "keep" to avoid removing PVCs during a helm delete
  207   # operation. Leaving it empty will delete PVCs after the chart deleted
  208   # (this does not apply for PVCs that are created for internal database
  209   # and redis components, i.e. they are never deleted automatically)
  210   resourcePolicy: "keep"
  211   persistentVolumeClaim:
  212     registry:
  213       # Use the existing PVC which must be created manually before bound,
  214       # and specify the "subPath" if the PVC is shared with other components
  215       existingClaim: "harbor-data"
  216       # Specify the "storageClass" used to provision the volume. Or the default
  217       # StorageClass will be used (the default).
  218       # Set it to "-" to disable dynamic provisioning
  219       storageClass: ""
  220       subPath: "registry"
  221       accessMode: ReadWriteOnce
  222       size: 5Gi
  223       annotations: {}
  224     chartmuseum:
  225       existingClaim: "harbor-data"
  226       storageClass: ""
  227       subPath: "chartmuseum"
  228       accessMode: ReadWriteOnce
  229       size: 5Gi
  230       annotations: {}
  
  
  246     # If external database is used, the following settings for database will
  247     # be ignored
  248     database:
  249       existingClaim: "harbor-data"
  250       storageClass: ""
  251       subPath: "database"
  252       accessMode: ReadWriteOnce
  253       size: 1Gi
  254       annotations: {}
  255     # If external Redis is used, the following settings for Redis will
  256     # be ignored
  257     redis:
  258       existingClaim: "harbor-data"
  259       storageClass: ""
  260       subPath: "redis"
  261       accessMode: ReadWriteOnce
  262       size: 1Gi
  263       annotations: {}
  264     trivy:
  265       existingClaim: "harbor-data"
  266       storageClass: ""
  267       subPath: "trivy"
  268       accessMode: ReadWriteOnce
  269       size: 5Gi
  270       annotations: {}
  ```

- 管理员账户密码（382行）

  ```yaml
  382 harborAdminPassword: "Harbor12345!"
  ```

- trivy、notary漏洞扫描组件，暂不启用（639，711行）

  ```yaml
  637 trivy:
  638   # enabled the flag to enable Trivy scanner
  639   enabled: false
  640   image:
  641     # repository the repository for Trivy adapter image
  642     repository: goharbor/trivy-adapter-photon
  643     # tag the tag for Trivy adapter image
  644     tag: v2.6.2
  
  
  710 notary:
  711   enabled: false
  712   server:
  713     # set the service account to be used, default if left empty
  714     serviceAccountName: ""
  715     # mount the service account token
  716     automountServiceAccountToken: false
  ```

helm创建：

```bash
# 使用本地chart安装
$ helm -n harbor install harbor ./harbor
```

###### [推送镜像到Harbor仓库](http://49.7.203.222:2023/#/kubernetes-advanced/helm?id=推送镜像到harbor仓库)

配置hosts及docker非安全仓库：

```bash
$ cat /etc/hosts
...
172.21.65.226 k8s-master harbor.luffy.com
...

$ cat /etc/docker/daemon.json
{                                            
  "insecure-registries": [                   
    "172.21.51.143:5000",                   
    "harbor.luffy.com"                     
  ],                                         
  "registry-mirrors" : [                     
    "https://8xpk5wnt.mirror.aliyuncs.com"   
  ]                                          
}                           

#
$ systemctl restart docker

# 使用账户密码登录admin/Harbor12345
$ docker login harbor.luffy.com

$ docker tag nginx:alpine harbor.luffy.com/library/nginx:alpine
$ docker push harbor.luffy.com/library/nginx:alpine


# containerd使用harbor.luffy.com
$ mkdir -p /etc/containerd/certs.d/harbor.luffy.com
$ cat /etc/containerd/certs.d/harbor.luffy.com/hosts.toml
server = "https://harbor.luffy.com"
[host."https://harbor.luffy.com"]
  capabilities = ["pull", "resolve", "push"]
  skip_verify = true

# 快速启动服务验证
$ kubectl create deployment test --image=harbor.luffy.com/library/nginx:alpine
```

###### [推送chart到Harbor仓库](http://49.7.203.222:2023/#/kubernetes-advanced/helm?id=推送chart到harbor仓库)

helm3默认没有安装helm push插件，需要手动安装。插件地址 https://github.com/chartmuseum/helm-push

安装插件：

```bash
$ helm plugin install https://github.com/chartmuseum/helm-push
```

离线安装：

```bash
$ mkdir helm-push
$ wget https://github.com/chartmuseum/helm-push/releases/download/v0.8.1/helm-push_0.8.1_linux_amd64.tar.gz
$ tar zxf helm-push_0.8.1_linux_amd64.tar.gz -C helm-push
$ helm plugin install ./helm-push
```

添加repo

```bash
$ helm repo add myharbor https://harbor.luffy.com/chartrepo/luffy
# x509错误

# 添加证书信任，根证书为配置给ingress使用的证书
$ kubectl get secret harbor-ingress -n harbor -o jsonpath="{.data.ca\.crt}" | base64 -d >harbor.ca.crt

$ cp harbor.ca.crt /etc/pki/ca-trust/source/anchors
$ update-ca-trust enable; update-ca-trust extract

# 再次添加
$ helm repo add luffy https://harbor.luffy.com/chartrepo/luffy --ca-file=harbor.ca.crt  --username admin --password Harbor12345!

$ helm repo ls
```

推送chart到仓库：

```bash
$ helm push harbor luffy --ca-file=harbor.ca.crt -u admin -p Harbor12345!

```



# [课程小结](http://49.7.203.222:2023/#/kubernetes-advanced/summary?id=课程小结)

使用k8s的进阶内容。

1. 学习k8s在etcd中数据的存储，掌握etcd的基本操作命令

2. 理解k8s调度的过程，预选及优先。影响调度策略的设置

   ![img](4Kubernetes进阶实践.assets/kube-scheduler-process-1669078918768155.png)

3. Flannel网络的原理学习，了解网络的流向，帮助定位问题

   ![img](4Kubernetes进阶实践.assets/pods-network-1669078918768157.webp)

4. 认证与授权，掌握kubectl、kubelet、rbac及二次开发如何调度API

   ![img](4Kubernetes进阶实践.assets/AUTH-1669078918768159.jpg)

5. 利用HPA进行业务动态扩缩容，通过metrics-server了解整个k8s的监控体系

   ![img](4Kubernetes进阶实践.assets/hpa-prometheus-custom-1669078918768161.png)

6. PV + PVC

   ![img](4Kubernetes进阶实践.assets/storage-class-1669078918768163.png)

7. Helm

   ![img](4Kubernetes进阶实践.assets/helm3.jpg)






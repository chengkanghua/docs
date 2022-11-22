# 非高可用版本



## 集群信息

### [节点规划](http://49.7.203.222:2023/#/install/single-master/cluster-info?id=节点规划)

部署k8s集群的节点按照用途可以划分为如下2类角色：

- **master**：集群的master节点，集群的初始化节点，基础配置不低于2C4G
- **slave**：集群的slave节点，可以多台，基础配置不低于2C4G

**本例为了演示slave节点的添加，会部署一台master+2台slave**，节点规划如下：

| 主机名     | 节点ip        | 角色   | 部署组件                                                     |
| ---------- | ------------- | ------ | ------------------------------------------------------------ |
| k8s-master | 172.21.65.226 | master | etcd, kube-apiserver, kube-controller-manager, kubectl, kubeadm, kubelet, kube-proxy, flannel |
| k8s-slave1 | 172.21.65.227 | slave  | kubectl, kubelet, kube-proxy, flannel                        |
| k8s-slave2 | 172.21.65.228 | slave  | kubectl, kubelet, kube-proxy, flannel                        |

### [组件版本](http://49.7.203.222:2023/#/install/single-master/cluster-info?id=组件版本)



| 组件       | 版本                              | 说明                                    |
| ---------- | --------------------------------- | --------------------------------------- |
| CentOS     | 7.8.2003                          |                                         |
| Kernel     | Linux 3.10.0-1127.10.1.el7.x86_64 |                                         |
| etcd       | 3.4.13-0                          | 使用Pod方式部署，默认数据挂载到本地路径 |
| coredns    | 1.7.0                             |                                         |
| kubeadm    | v1.24.4                           |                                         |
| kubectl    | v1.24.4                           |                                         |
| kubelet    | v1.24.4                           |                                         |
| kube-proxy | v1.24.4                           |                                         |
| flannel    | v0.19.2                           |                                         |

## 安装前准备

### [设置hosts解析](http://49.7.203.222:2023/#/install/single-master/prepare?id=设置hosts解析)

操作节点：所有节点（`k8s-master，k8s-slave`）均需执行

- **修改hostname** hostname必须只能包含小写字母、数字、","、"-"，且开头结尾必须是小写字母或数字

```python
# 在master节点
$ hostnamectl set-hostname k8s-master #设置master节点的hostname

# 在slave-1节点
$ hostnamectl set-hostname k8s-slave1 #设置slave1节点的hostname

# 在slave-2节点
$ hostnamectl set-hostname k8s-slave2 #设置slave2节点的hostname
```

- **添加hosts解析**

```python
$ cat >>/etc/hosts<<EOF
172.21.65.226 k8s-master
172.21.65.227 k8s-slave1
172.21.65.228 k8s-slave2
EOF
```

### [调整系统配置](http://49.7.203.222:2023/#/install/single-master/prepare?id=调整系统配置)

操作节点： 所有的master和slave节点（`k8s-master,k8s-slave`）需要执行

> 本章下述操作均以k8s-master为例，其他节点均是相同的操作（ip和hostname的值换成对应机器的真实值）

- **设置安全组开放端口**

如果节点间无安全组限制（内网机器间可以任意访问），可以忽略，否则，至少保证如下端口可通： k8s-master节点：TCP：6443，2379，2380，60080，60081UDP协议端口全部打开 k8s-slave节点：UDP协议端口全部打开

- **设置iptables**

```python
iptables -P FORWARD ACCEPT
```

- **关闭swap**

```python
swapoff -a
# 防止开机自动挂载 swap 分区
sed -i '/ swap / s/^\(.*\)$/#\1/g' /etc/fstab
```

- **关闭selinux和防火墙**

```python
sed -ri 's#(SELINUX=).*#\1disabled#' /etc/selinux/config
setenforce 0
systemctl disable firewalld && systemctl stop firewalld
```

- **修改内核参数**

```python
cat <<EOF >  /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
net.ipv4.ip_forward=1
vm.max_map_count=262144
EOF
modprobe br_netfilter
sysctl -p /etc/sysctl.d/k8s.conf
```

- 设置yum源

```bash
$ curl -o /etc/yum.repos.d/Centos-7.repo http://mirrors.aliyun.com/repo/Centos-7.repo
$ curl -o /etc/yum.repos.d/docker-ce.repo http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
$ cat <<EOF > /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=http://mirrors.aliyun.com/kubernetes/yum/repos/kubernetes-el7-x86_64
enabled=1
gpgcheck=0
repo_gpgcheck=0
gpgkey=http://mirrors.aliyun.com/kubernetes/yum/doc/yum-key.gpg
        http://mirrors.aliyun.com/kubernetes/yum/doc/rpm-package-key.gpg
EOF
$ yum clean all && yum makecache
```

### [安装docker](http://49.7.203.222:2023/#/install/single-master/prepare?id=安装docker)

操作节点： 所有节点

```python
 ## 查看所有的可用版本
$ yum list docker-ce --showduplicates | sort -r
##安装旧版本 yum install docker-ce-cli-18.09.9-3.el7  docker-ce-18.09.9-3.el7
## 安装源里最新版本
$ yum install docker-ce-20.10.18 -y

## 配置docker加速和非安全的镜像仓库，需要根据个人的实际环境修改
$ mkdir -p /etc/docker
vi /etc/docker/daemon.json
{
  "insecure-registries": [    
    "172.21.65.226:5000" 
  ],                          
  "registry-mirrors" : [
    "https://8xpk5wnt.mirror.aliyuncs.com"
  ]
}
## 启动docker
$ systemctl enable docker && systemctl start docker
```


## 初始化集群

### [安装 kubeadm, kubelet 和 kubectl](http://49.7.203.222:2023/#/install/single-master/init?id=安装-kubeadm-kubelet-和-kubectl)

操作节点： 所有的master和slave节点(`k8s-master,k8s-slave`) 需要执行

```bash
$ yum install -y kubelet-1.24.4 kubeadm-1.24.4 kubectl-1.24.4 --disableexcludes=kubernetes
## 查看kubeadm 版本
$ kubeadm version
## 设置kubelet开机启动
$ systemctl enable kubelet 
```

### [配置containerd](http://49.7.203.222:2023/#/install/single-master/init?id=配置containerd)

操作节点：所有的master和slave节点(`k8s-master,k8s-slave`) 需要执行

- 将 `sandbox_image` 镜像源设置为阿里云`google_containers`镜像源：

  ```bash
  # 导出默认配置，config.toml这个文件默认是不存在的
  containerd config default > /etc/containerd/config.toml
  grep sandbox_image  /etc/containerd/config.toml
  sed -i "s#k8s.gcr.io/pause#registry.aliyuncs.com/google_containers/pause#g"       /etc/containerd/config.toml
  sed -i "s#registry.k8s.io/pause#registry.aliyuncs.com/google_containers/pause#g"       /etc/containerd/config.toml
  ```

- 配置containerd cgroup 驱动程序systemd：

  ```bash
  sed -i 's#SystemdCgroup = false#SystemdCgroup = true#g' /etc/containerd/config.toml
  ```

- 配置`docker hub`镜像加速：

  ```bash
  # 修改配置文件/etc/containerd/config.toml, 145行添加config_path
  ...
      144     [plugins."io.containerd.grpc.v1.cri".registry]
      145       config_path = "/etc/containerd/certs.d"
      146
      147       [plugins."io.containerd.grpc.v1.cri".registry.auths]
      148
      149       [plugins."io.containerd.grpc.v1.cri".registry.configs]
      150
      151       [plugins."io.containerd.grpc.v1.cri".registry.headers]
      152
      153       [plugins."io.containerd.grpc.v1.cri".registry.mirrors]
  ...
  
  # 创建对应的目录
  mkdir -p /etc/containerd/certs.d/docker.io
  
  # 配置加速
  cat >/etc/containerd/certs.d/docker.io/hosts.toml <<EOF
  server = "https://docker.io"
  [host."https://8xpk5wnt.mirror.aliyuncs.com"]
    capabilities = ["pull","resolve"]
  [host."https://docker.mirrors.ustc.edu.cn"]
    capabilities = ["pull","resolve"]
  [host."https://registry-1.docker.io"]
    capabilities = ["pull","resolve","push"]
  EOF
  ```

- 配置非安全的私有镜像仓库：

  ```bash
  # 此处目录必须和个人环境中实际的仓库地址保持一致
  mkdir -p /etc/containerd/certs.d/172.21.65.226:5000
  cat >/etc/containerd/certs.d/172.21.65.226:5000/hosts.toml <<EOF
  server = "http://172.21.65.226:5000"
  [host."http://172.21.65.226:5000"]
    capabilities = ["pull", "resolve", "push"]
    skip_verify = true
  EOF
  ```

- 应用所有更改后,重新启动containerd：

  ```bash
  systemctl restart containerd
  ```

### [初始化配置文件](http://49.7.203.222:2023/#/install/single-master/init?id=初始化配置文件)

操作节点： 只在master节点（`k8s-master`）执行

```yaml
$ kubeadm config print init-defaults > kubeadm.yaml
$ cat kubeadm.yaml
apiVersion: kubeadm.k8s.io/v1beta3
bootstrapTokens:
- groups:
  - system:bootstrappers:kubeadm:default-node-token
  token: abcdef.0123456789abcdef
  ttl: 24h0m0s
  usages:
  - signing
  - authentication
kind: InitConfiguration
localAPIEndpoint:
  advertiseAddress: 172.21.65.226   # 此处替换为k8s-master的ip地址
  bindPort: 6443
nodeRegistration:
  criSocket: unix:///var/run/containerd/containerd.sock
  imagePullPolicy: IfNotPresent
  name: k8s-master                    # 此处替换为k8s-master的hostname
  taints: null
---
apiServer:
  timeoutForControlPlane: 4m0s
apiVersion: kubeadm.k8s.io/v1beta3
certificatesDir: /etc/kubernetes/pki
clusterName: kubernetes
controllerManager: {}
dns: {}
etcd:
  local:
    dataDir: /var/lib/etcd
imageRepository: registry.aliyuncs.com/google_containers   # 替换为国内镜像源
kind: ClusterConfiguration
kubernetesVersion: 1.24.4              # 替换为1.24.4
networking:
  dnsDomain: cluster.local
  podSubnet: 10.244.0.0/16              # 添加此行，用来分配k8s节点的pod ip
  serviceSubnet: 10.96.0.0/12
scheduler: {}
```

> 对于上面的资源清单的文档比较杂，要想完整了解上面的资源对象对应的属性，可以查看对应的 godoc 文档，地址: https://godoc.org/k8s.io/kubernetes/cmd/kubeadm/app/apis/kubeadm/v1beta3。

### [提前下载镜像](http://49.7.203.222:2023/#/install/single-master/init?id=提前下载镜像)

操作节点：只在master节点（`k8s-master`）执行

```python
  # 查看需要使用的镜像列表,若无问题，将得到如下列表
$ kubeadm config images list --config kubeadm.yaml
registry.aliyuncs.com/google_containers/kube-apiserver:v1.24.4
registry.aliyuncs.com/google_containers/kube-controller-manager:v1.24.4
registry.aliyuncs.com/google_containers/kube-scheduler:v1.24.4
registry.aliyuncs.com/google_containers/kube-proxy:v1.24.4
registry.aliyuncs.com/google_containers/pause:3.7
registry.aliyuncs.com/google_containers/etcd:3.5.3-0
registry.aliyuncs.com/google_containers/coredns:v1.8.6
  # 提前下载镜像到本地
$ kubeadm config images pull --config kubeadm.yaml
[config/images] Pulled registry.aliyuncs.com/google_containers/kube-apiserver:v1.24.4
[config/images] Pulled registry.aliyuncs.com/google_containers/kube-controller-manager:v1.24.4
[config/images] Pulled registry.aliyuncs.com/google_containers/kube-scheduler:v1.24.4
[config/images] Pulled registry.aliyuncs.com/google_containers/kube-proxy:v1.24.4
[config/images] Pulled registry.aliyuncs.com/google_containers/pause:3.7
[config/images] Pulled registry.aliyuncs.com/google_containers/etcd:3.5.3-0
[config/images] Pulled registry.aliyuncs.com/google_containers/coredns:v1.8.6
```

### [初始化master节点](http://49.7.203.222:2023/#/install/single-master/init?id=初始化master节点)

操作节点：只在master节点（`k8s-master`）执行，注意只在master节点执行！

```python
$ kubeadm init --config kubeadm.yaml
```

若初始化成功后，最后会提示如下信息：

```python
...
Your Kubernetes master has initialized successfully!

To start using your cluster, you need to run the following as a regular user:

  mkdir -p $HOME/.kube
  sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
  sudo chown $(id -u):$(id -g) $HOME/.kube/config

You should now deploy a pod network to the cluster.
Run "kubectl apply -f [podnetwork].yaml" with one of the options listed at:
  https://kubernetes.io/docs/concepts/cluster-administration/addons/

Then you can join any number of worker nodes by running the following on each as root:

kubeadm join 172.21.65.226:6443 --token abcdef.0123456789abcdef \
    --discovery-token-ca-cert-hash sha256:1c4305f032f4bf534f628c32f5039084f4b103c922ff71b12a5f0f98d1ca9a4f
```

接下来按照上述提示信息操作，配置kubectl客户端的认证

```python
  mkdir -p $HOME/.kube
  cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
  chown $(id -u):$(id -g) $HOME/.kube/config
```

> **⚠️注意：**此时使用 kubectl get nodes查看节点应该处于notReady状态，因为还未配置网络插件
>
> 若执行初始化过程中出错，根据错误信息调整后，执行kubeadm reset后再次执行init操作即可

### [添加slave节点到集群中](http://49.7.203.222:2023/#/install/single-master/init?id=添加slave节点到集群中)

操作节点：所有的slave节点（`k8s-slave`）需要执行 在每台slave节点，执行如下命令，该命令是在kubeadm init成功后提示信息中打印出来的，需要替换成实际init后打印出的命令。

```python
kubeadm join 172.21.65.226:6443 --token abcdef.0123456789abcdef \
    --discovery-token-ca-cert-hash sha256:1c4305f032f4bf534f628c32f5039084f4b103c922ff71b12a5f0f98d1ca9a4f
```

如果忘记添加命令，可以通过如下命令生成：

```bash
$ kubeadm token create --print-join-command
```



## 网络插件

操作节点：只在master节点（`k8s-master`）执行，CNI

- 下载flannel的yaml文件

  ```bash
  wget https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml
  ```

- 修改配置，指定网卡名称，大概在文件的159行，添加一行配置：

  ```bash
  $ vi kube-flannel.yml
  ...      
  150       containers:
  151       - name: kube-flannel
  152        #image: flannelcni/flannel:v0.19.2 for ppc64le and mips64le (dockerhub limitations may apply)
  153         image: docker.io/rancher/mirrored-flannelcni-flannel:v0.19.2
  154         command:
  155         - /opt/bin/flanneld
  156         args:
  157         - --ip-masq
  158         - --kube-subnet-mgr
  159         - --iface=eth0   # 如果机器存在多网卡的话，指定内网网卡的名称，默认不指定的话会找第一块网卡
  160         resources:
  161           requests:
  162             cpu: "100m"
  163             memory: "50Mi"
  ...
  ```

- 确认pod网段

  ```bash
  vi kube-flannel.yml
   82   net-conf.json: |
   83     {
   84       "Network": "10.244.0.0/16",
   85       "Backend": {
   86         "Type": "vxlan"
   87       }
   88     }
   
  # 确认84行的网段和前面kubeadm.yaml中初始化使用的配置中的podSubnet保持一致！
  ```

- 执行安装flannel网络插件

  ```bash
  # 执行flannel安装
  kubectl apply -f kube-flannel.yml
  kubectl -n kube-flannel get po -owide
  ```



## 集群设置

### [设置master节点是否可调度（可选）](http://49.7.203.222:2023/#/install/single-master/cluster-setting?id=设置master节点是否可调度（可选）)

操作节点：`k8s-master`

默认部署成功后，master节点无法调度业务pod，如需设置master节点也可以参与pod的调度，需执行：

```bash
kubectl taint node k8s-master node-role.kubernetes.io/master:NoSchedule-
kubectl taint node k8s-master node-role.kubernetes.io/control-plane:NoSchedule-
```

> 课程后期会部署系统组件到master节点，因此，此处建议设置k8s-master节点为可调度

### [设置kubectl自动补全](http://49.7.203.222:2023/#/install/single-master/cluster-setting?id=设置kubectl自动补全)

操作节点：`k8s-master`

```bash
$ yum install bash-completion -y
$ source /usr/share/bash-completion/bash_completion
$ source <(kubectl completion bash)
$ echo "source <(kubectl completion bash)" >> ~/.bashrc
```



## 调整证书过期

使用kubeadm安装的集群，证书默认有效期为1年，可以通过如下方式修改为10年。

```bash
cd /etc/kubernetes/pki

# 查看当前证书有效期
for i in $(ls *.crt); do echo "===== $i ====="; openssl x509 -in $i -text -noout | grep -A 3 'Validity' ; done

mkdir backup_key; cp -rp ./* backup_key/
git clone https://github.com/yuyicai/update-kube-cert.git
cd update-kube-cert/ 
bash update-kubeadm-cert.sh all

#若无法clone项目，可以手动在浏览器中打开后，复制update-kubeadm-cert.sh 脚本内容到机器中执行

```

## 验证集群

操作节点： 在master节点（`k8s-master`）执行

```python
$ kubectl get nodes  #观察集群节点是否全部Ready
```

创建测试nginx服务

```python
$ kubectl run  test-nginx --image=nginx:alpine
```

查看pod是否创建成功，并访问pod ip测试是否可用

```bash
$ kubectl get po -o wide
NAME                          READY   STATUS    RESTARTS   AGE   IP           NODE         NOMINATED NODE   READINESS GATES
test-nginx-5bd8859b98-5nnnw   1/1     Running   0          9s    10.244.1.2   k8s-slave1   <none>           <none>
$ curl 10.244.1.2
...
<h1>Welcome to nginx!</h1>
<p>If you see this page, the nginx web server is successfully installed and
working. Further configuration is required.</p>

<p>For online documentation and support please refer to
<a href="http://nginx.org/">nginx.org</a>.<br/>
Commercial support is available at
<a href="http://nginx.com/">nginx.com</a>.</p>

<p><em>Thank you for using nginx.</em></p>
</body>
</html>
```



## containerd客户端介绍

操作节点：所有节点

由于新版本的k8s直接采用`containerd`作为容器运行时，因此，后续创建的服务，通过`docker`的命令无法查询，因此，如果有需要对节点中的容器进行操作的需求，需要用`containerd`的命令行工具来替换，目前总共有三种，包含：

- ctr
- crictl
- nerctl

###### [ctr](http://49.7.203.222:2023/#/install/single-master/containerd-cli?id=ctr)

ctr为最基础的`containerd`的操作命令行工具，安装`containerd`时已默认安装，因此无需再单独安装。

ctr的可操作的命令很少，且很不人性化，因此极力不推荐使用

Containerd 也有 namespaces 的概念，对于上层编排系统的支持，`ctr` 客户端 主要区分了 3 个命名空间分别是`k8s.io`、`moby`和`default`

比如操作容器和镜像：

```bash
# 查看containerd的命名空间
ctr ns ls;

# 查看containerd启动的容器列表
ctr -n k8s.io container ls

# 查看镜像列表
ctrl -n k8s.io image ls

# 导入镜像
ctr -n=k8s.io image import dashboard.tar

# 从私有仓库拉取镜像，前提是/etc/containerd/certs.d下已经配置过该私有仓库的非安全认证
ctr images pull --user admin:admin  --hosts-dir "/etc/containerd/certs.d"  172.21.65.226:5000/eladmin/eladmin-api:v1-rc1

# ctr命令无法查看容器的日志，也无法执行exec等操作
```

###### [crictl](http://49.7.203.222:2023/#/install/single-master/containerd-cli?id=crictl)

`crictl` 是遵循 CRI 接口规范的一个命令行工具，通常用它来检查和管理kubelet节点上的容器运行时和镜像。

主机安装了 k8s 后，命令行会有` crictl` 命令，无需单独安装。

`crictl` 命令默认使用`k8s.io` 这个名称空间，因此无需单独指定，使用前，需要先加一下配置文件：

```bash
cat /etc/crictl.yaml
runtime-endpoint: unix:///run/containerd/containerd.sock
image-endpoint: unix:///run/containerd/containerd.sock
timeout: 10
debug: false
```

常用操作：

```bash
# 查看容器列表
crictl ps

# 查看镜像列表
crictl images 

# 删除镜像
crictl rmi 172.21.65.226:5000/eladmin/eladmin-api:v1-rc1

# 拉取镜像， 若拉取私有镜像，需要修改containerd配置添加认证信息，比较麻烦且不安全
crictl pull nginx:alpine

# 执行exec操作
crictl ps 
CONTAINER           IMAGE               CREATED             STATE               NAME                      ATTEMPT             POD ID              POD
d23fe516d2eeb       8b0e63fd4fec6       5 hours ago         Running             eladmin-api               0                   5dbae572dcb6b       eladmin-api-5d979bb778-tc5kz

# 注意只能使用containerid
crictl exec -ti d23fe516d2eeb bash

# 查看容器日志
crictl logs -f d23fe516d2eeb

# 清理镜像
crictl rmi --prune
```

###### [nerdctl](http://49.7.203.222:2023/#/install/single-master/containerd-cli?id=nerdctl)

推荐使用 `nerdctl`，使用效果与 docker 命令的语法基本一致 , 官网`https://github.com/containerd/nerdctl`

安装：

```bash
# 下载精简版安装包，精简版的包无法使用nerdctl进行构建镜像
wget https://github.com/containerd/nerdctl/releases/download/v0.23.0/nerdctl-0.23.0-linux-amd64.tar.gz

#如果下载超时或者速度慢，也可以去网盘自取
链接: https://pan.baidu.com/s/14Q2tPbiNXdN-PLKk1hpKhA 提取码: 496v 

# 解压后，将nerdctl 命令拷贝至$PATH下即可
cp nerdctl /usr/bin/
```

常用操作：

```bash
# 查看镜像列表
nerdctl -n k8s.io ps -a

# 执行exec
nerdctl -n k8s.io exec -ti e2cd02190005 sh

# 登录镜像仓库
nerdctl login 172.21.65.226:5000

# 拉取镜像,如果是想拉取了让k8s使用，一定加上-n k8s.io,否则会拉取到default空间中， k8s默认只使用k8s.io
nerdctl -n k8s.io pull 172.21.65.226:5000/eladmin/eladmin-api:v1-rc1


# 启动容器
nerdctl -n k8s.io run -d --name test nginx:alpine

# exec
nerdctl -n k8s.io  exec -ti test sh

# 查看日志, 注意，nerdctl 只能查看使用nerdctl命令创建从容器的日志，k8s中kubelet创建的产生的容器无法查看
nerdctl -n k8s.io logs -f test

# 构建，但是需要额外安装buildkit的包
nerdctl build . -t xxxx:tag -f Dockerfile
```

###### [使用小经验](http://49.7.203.222:2023/#/install/single-master/containerd-cli?id=使用小经验)

- 用了k8s后，对于业务应用的基本操作，90%以上都可以通过`kubectl`命令行完成
- 对于镜像的构建，仍然推荐使用`docker build` 来完成，推送到镜像仓库后，containerd可以直接使用
- 对于查看containerd中容器的日志，使用 `crictl logs`完成，因为ctr、nerdctl均不支持
- 对于其他常规的containerd容器操作，建议使用nerdctl完成

更多命令可以参考下文：

- https://www.modb.pro/db/485911
- https://github.com/containerd/nerdctl#container-management



## [部署dashboard](http://49.7.203.222:2023/#/install/single-master/dashboard?id=部署dashboard)

- 部署服务

```bash
# 推荐使用下面这种方式
$ wget https://raw.githubusercontent.com/kubernetes/dashboard/v2.2.0/aio/deploy/recommended.yaml
$ vi recommended.yaml
# 修改Service为NodePort类型，文件的45行上下
......
kind: Service
apiVersion: v1
metadata:
  labels:
    k8s-app: kubernetes-dashboard
  name: kubernetes-dashboard
  namespace: kubernetes-dashboard
spec:
  ports:
    - port: 443
      targetPort: 8443
  selector:
    k8s-app: kubernetes-dashboard
  type: NodePort  # 加上type=NodePort变成NodePort类型的服务
......
```

- 查看访问地址，本例为30133端口

```bash
$ kubectl apply -f recommended.yaml
$ kubectl -n kubernetes-dashboard get svc
NAME                        TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)         AGE
dashboard-metrics-scraper   ClusterIP   10.105.62.124   <none>        8000/TCP        31m
kubernetes-dashboard        NodePort    10.103.74.46    <none>        443:30133/TCP   31m 
```

- 使用浏览器访问 [https://172.21.51.143:30133，其中172.21.51.143为master节点的外网ip地址，chrome目前由于安全限制，默认访问受限制，在chrome浏览器页面点击任意空白处，直接键盘输入“thisisunsafe”即可进行访问。](https://172.21.51.143:30133，其中172.21.51.143为master节点的外网ip地址，chrome目前由于安全限制，默认访问受限制，在chrome浏览器页面点击任意空白处，直接键盘输入“thisisunsafe”即可进行访问。/)
- 创建ServiceAccount进行访问

```bash
$ vi dashboard-admin.conf
kind: ClusterRoleBinding
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: admin
  annotations:
    rbac.authorization.kubernetes.io/autoupdate: "true"
roleRef:
  kind: ClusterRole
  name: cluster-admin
  apiGroup: rbac.authorization.k8s.io
subjects:
- kind: ServiceAccount
  name: admin
  namespace: kubernetes-dashboard

---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: admin
  namespace: kubernetes-dashboard

$ kubectl apply -f dashboard-admin.conf
# 创建访问token
$ kubectl -n kubernetes-dashboard create token admin
eyJhbGciOiJSUzI1NiIsImtpZCI6Ik1rb2xHWHMwbWFPMjJaRzhleGRqaExnVi1BLVNRc2txaEhETmVpRzlDeDQifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlcm5ldGVzLWRhc2hib2FyZCIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJhZG1pbi10b2tlbi1mcWRwZiIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50Lm5hbWUiOiJhZG1pbiIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6IjYyNWMxNjJlLTQ1ZG...
```

![img](2Kubernetes安装文档.assets/dashboard.png)

![img](2Kubernetes安装文档.assets/dashboard-content.jpg)



## 清理集群

如果你的集群安装过程中遇到了其他问题，我们可以使用下面的命令来进行重置：

```bash
# 在全部集群节点执行
kubeadm reset
ifconfig cni0 down && ip link delete cni0
ifconfig flannel.1 down && ip link delete flannel.1
rm -rf /run/flannel/subnet.env
rm -rf /var/lib/cni/
mv /etc/kubernetes/ /tmp
mv /var/lib/etcd /tmp
mv ~/.kube /tmp
iptables -F
iptables -t nat -F
ipvsadm -C
ip link del kube-ipvs0
ip link del dummy0
```





# 高可用版本

## 集群信息

### [1. 节点规划](http://49.7.203.222:2023/#/install/multi-master/cluster-info?id=_1-节点规划)

部署k8s集群的节点按照用途可以划分为如下2类角色：

- **master**：集群的master节点，集群的初始化节点，基础配置不低于2C4G
- **node**：集群的node节点，可以多台，基础配置不低于2C4G

**本例为了演示node节点的添加，会部署一台master+2台node**，节点规划如下：

| 主机名      | 节点ip        | 角色   | 部署组件                                                     |
| ----------- | ------------- | ------ | ------------------------------------------------------------ |
| k8s-master1 | 172.21.51.67  | master | etcd, kube-apiserver, kube-controller-manager, kubectl, kubeadm, kubelet, kube-proxy, flannel |
| k8s-master2 | 172.21.51.68  | master | etcd, kube-apiserver, kube-controller-manager, kubectl, kubeadm, kubelet, kube-proxy, flannel |
| k8s-master3 | 172.21.51.55  | master | etcd, kube-apiserver, kube-controller-manager, kubectl, kubeadm, kubelet, kube-proxy, flannel |
|             | 172.21.51.120 | VIP    | 作为3台master节点的LB使用                                    |
| k8s-node1   | 172.21.51.143 | node   | kubectl, kubelet, kube-proxy, flannel                        |
| k8s-node2   | 172.21.52.84  | node   | kubectl, kubelet, kube-proxy, flannel                        |

### [2. 组件版本](http://49.7.203.222:2023/#/install/multi-master/cluster-info?id=_2-组件版本)



| 组件       | 版本                              | 说明                                    |
| ---------- | --------------------------------- | --------------------------------------- |
| CentOS     | 7.8.2003                          |                                         |
| Kernel     | Linux 3.10.0-1127.10.1.el7.x86_64 |                                         |
| etcd       | 3.4.13-0                          | 使用Pod方式部署，默认数据挂载到本地路径 |
| coredns    | 1.8.0                             |                                         |
| kubeadm    | v1.24.4                           |                                         |
| kubectl    | v1.24.4                           |                                         |
| kubelet    | v1.24.4                           |                                         |
| kube-proxy | v1.24.4                           |                                         |
| flannel    | v0.11.0                           |                                         |



## 安装前准备

### [1. 设置hosts解析](http://49.7.203.222:2023/#/install/multi-master/prepare?id=_1-设置hosts解析)

操作节点：所有节点（`k8s-master，k8s-node`）均需执行

- **修改hostname** hostname必须只能包含小写字母、数字、","、"-"，且开头结尾必须是小写字母或数字

```python
# 以其中一台master和node为例：

# 在k8s-master1节点
$ hostnamectl set-hostname k8s-master1 #设置master节点的hostname

# 在node-1节点
$ hostnamectl set-hostname k8s-node1 #设置node1节点的hostname
```

- **添加hosts解析**

```python
$ cat >>/etc/hosts<<EOF
172.21.51.67 k8s-master1
172.21.51.68 k8s-master2
172.21.51.50 k8s-master3
172.21.51.143 k8s-node1
172.21.52.84 k8s-node2
EOF
```

### [2. 调整系统配置](http://49.7.203.222:2023/#/install/multi-master/prepare?id=_2-调整系统配置)

操作节点： 所有的master和node节点（`k8s-master,k8s-node`）需要执行

> 本章下述操作均以k8s-master为例，其他节点均是相同的操作（ip和hostname的值换成对应机器的真实值）

- **设置安全组开放端口**

如果节点间无安全组限制（内网机器间可以任意访问），可以忽略，否则，至少保证如下端口可通： k8s-master节点：TCP：6443，2379，2380，60080，60081UDP协议端口全部打开 k8s-node节点：UDP协议端口全部打开

- **设置iptables**

```python
iptables -P FORWARD ACCEPT
```

- **关闭swap**

```python
swapoff -a && sysctl -w vm.swappiness=0
# 防止开机自动挂载 swap 分区
sed -i '/ swap / s/^\(.*\)$/#\1/g' /etc/fstab
```

- **关闭selinux和防火墙**

```python
sed -ri 's#(SELINUX=).*#\1disabled#' /etc/selinux/config
setenforce 0
systemctl disable firewalld && systemctl stop firewalld
```

- **修改内核参数**

```python
cat <<EOF >  /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
net.ipv4.ip_forward=1
vm.max_map_count=262144
net.ipv4.ip_forward = 1
net.bridge.bridge-nf-call-iptables = 1
net.bridge.bridge-nf-call-ip6tables = 1
fs.may_detach_mounts = 1
vm.overcommit_memory=1
vm.panic_on_oom=0
fs.inotify.max_user_watches=89100
fs.file-max=52706963
fs.nr_open=52706963
net.netfilter.nf_conntrack_max=2310720
net.ipv4.tcp_keepalive_time = 600
net.ipv4.tcp_keepalive_probes = 3
net.ipv4.tcp_keepalive_intvl =15
net.ipv4.tcp_max_tw_buckets = 36000
net.ipv4.tcp_tw_reuse = 1
net.ipv4.tcp_max_orphans = 327680
net.ipv4.tcp_orphan_retries = 3
net.ipv4.tcp_syncookies = 1
net.ipv4.tcp_max_syn_backlog = 16384
net.ipv4.ip_conntrack_max = 65536
net.ipv4.tcp_max_syn_backlog = 16384
net.ipv4.tcp_timestamps = 0
net.core.somaxconn = 16384
EOF
modprobe br_netfilter
sysctl -p /etc/sysctl.d/k8s.conf
```

- 设置yum源

```bash
$ curl -o /etc/yum.repos.d/Centos-7.repo http://mirrors.aliyun.com/repo/Centos-7.repo
$ curl -o /etc/yum.repos.d/docker-ce.repo http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
$ cat <<EOF > /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=http://mirrors.aliyun.com/kubernetes/yum/repos/kubernetes-el7-x86_64
enabled=1
gpgcheck=0
repo_gpgcheck=0
gpgkey=http://mirrors.aliyun.com/kubernetes/yum/doc/yum-key.gpg
        http://mirrors.aliyun.com/kubernetes/yum/doc/rpm-package-key.gpg
EOF
$ yum clean all && yum makecache
$ yum install ipvsadm ipset sysstat conntrack libseccomp -y
```

### [3. 安装docker](http://49.7.203.222:2023/#/install/multi-master/prepare?id=_3-安装docker)

操作节点： 所有节点

```python
 ## 查看所有的可用版本
$ yum list docker-ce --showduplicates | sort -r
##安装旧版本 yum install docker-ce-cli-18.09.9-3.el7  docker-ce-18.09.9-3.el7
## 安装源里最新版本
$ yum install docker-ce-20.10.18 -y

## 配置docker加速
$ mkdir -p /etc/docker
vi /etc/docker/daemon.json
{
  "insecure-registries": [    
    "172.21.51.67:5000" 
  ],                          
  "registry-mirrors" : [
    "https://8xpk5wnt.mirror.aliyuncs.com"
  ],
  "exec-opts": ["native.cgroupdriver=systemd"]
}
## 启动docker
$ systemctl enable docker && systemctl start docker
```



## 初始化集群

### [安装 kubeadm, kubelet 和 kubectl](http://49.7.203.222:2023/#/install/multi-master/init?id=安装-kubeadm-kubelet-和-kubectl)

操作节点： 所有的master和node节点(`k8s-master,k8s-node`) 需要执行

```bash
$ yum install -y kubelet-1.24.4 kubeadm-1.24.4 kubectl-1.24.4 --disableexcludes=kubernetes
## 查看kubeadm 版本
$ kubeadm version
## 设置kubelet开机启动
$ systemctl enable kubelet 
```

### [配置containerd](http://49.7.203.222:2023/#/install/multi-master/init?id=配置containerd)

操作节点：所有的master和slave节点(`k8s-master,k8s-slave`) 需要执行

- 将 `sandbox_image` 镜像源设置为阿里云`google_containers`镜像源：

  ```bash
  # 导出默认配置，config.toml这个文件默认是不存在的
  containerd config default > /etc/containerd/config.toml
  grep sandbox_image  /etc/containerd/config.toml
  sed -i "s#k8s.gcr.io/pause#registry.aliyuncs.com/google_containers/pause#g"       /etc/containerd/config.toml
  sed -i "s#registry.k8s.io/pause#registry.aliyuncs.com/google_containers/pause#g"       /etc/containerd/config.toml
  ```

- 配置containerd cgroup 驱动程序systemd：

  ```bash
  sed -i 's#SystemdCgroup = false#SystemdCgroup = true#g' /etc/containerd/config.toml
  ```

- 配置`docker hub`镜像加速：

  ```bash
  # 修改配置文件/etc/containerd/config.toml, 145行添加config_path
  ...
      144     [plugins."io.containerd.grpc.v1.cri".registry]
      145       config_path = "/etc/containerd/certs.d"
      146
      147       [plugins."io.containerd.grpc.v1.cri".registry.auths]
      148
      149       [plugins."io.containerd.grpc.v1.cri".registry.configs]
      150
      151       [plugins."io.containerd.grpc.v1.cri".registry.headers]
      152
      153       [plugins."io.containerd.grpc.v1.cri".registry.mirrors]
  ...
  
  # 创建对应的目录
  mkdir -p /etc/containerd/certs.d/docker.io
  
  # 配置加速
  cat >/etc/containerd/certs.d/docker.io/hosts.toml <<EOF
  server = "https://docker.io"
  [host."https://8xpk5wnt.mirror.aliyuncs.com"]
    capabilities = ["pull","resolve"]
  [host."https://docker.mirrors.ustc.edu.cn"]
    capabilities = ["pull","resolve"]
  [host."https://registry-1.docker.io"]
    capabilities = ["pull","resolve","push"]
  EOF
  ```

- 配置非安全的私有镜像仓库：

  ```bash
  # 此处目录必须和个人环境中实际的仓库地址保持一致
  mkdir -p /etc/containerd/certs.d/172.21.65.226:5000
  cat >/etc/containerd/certs.d/172.21.65.226:5000/hosts.toml <<EOF
  server = "http://172.21.51.67:5000"
  [host."http://172.21.51.67:5000"]
    capabilities = ["pull", "resolve", "push"]
    skip_verify = true
  EOF
  ```

- 应用所有更改后,重新启动containerd：

  ```bash
  systemctl restart containerd
  ```

### [安装配置haproxy、keepalived](http://49.7.203.222:2023/#/install/multi-master/init?id=安装配置haproxy、keepalived)

操作节点： 所有的master

```bash
$ yum install keepalived haproxy -y

# 所有master节点执行,注意替换最后的master节点IP地址
$ vi /etc/haproxy/haproxy.cfg
global
  maxconn  2000
  ulimit-n  16384
  log  127.0.0.1 local0 err
  stats timeout 30s
defaults
  log global
  mode  http
  option  httplog
  timeout connect 5000
  timeout client  50000
  timeout server  50000
  timeout http-request 15s
timeout http-keep-alive 15s
frontend monitor-in
  bind *:33305
  mode http
  option httplog
  monitor-uri /monitor
frontend k8s-master
  bind 0.0.0.0:7443
  bind 127.0.0.1:7443
  mode tcp
  option tcplog
  tcp-request inspect-delay 5s
  default_backend k8s-master
backend k8s-master
  mode tcp
  option tcplog
  option tcp-check
  balance roundrobin
  default-server inter 10s downinter 5s rise 2 fall 2 slowstart 60s maxconn 250 maxqueue 256 weight 100
  server k8s-master1    172.21.51.67:6443  check
  server k8s-master2    172.21.51.68:6443   check
  server k8s-master3    172.21.51.55:6443   check 
  
  
# 在k8s-master1节点，注意mcast_src_ip换成实际的master1ip地址，virtual_ipaddress换成lb地址
$ vi /etc/keepalived/keepalived.conf
! Configuration File for keepalived
global_defs {
    router_id LVS_DEVEL
script_user root
    enable_script_security
}
vrrp_script chk_apiserver {
    script "/etc/keepalived/check_apiserver.sh"
    interval 5
    weight -5
    fall 2
    rise 1
}
vrrp_instance VI_1 {
    state MASTER
    interface eth0
    mcast_src_ip 172.21.51.67
    virtual_router_id 60
    priority 101
    advert_int 2
    authentication {
        auth_type PASS
        auth_pass K8SHA_KA_AUTH
    }
    virtual_ipaddress {
        172.21.51.120
    }
    track_script {
       chk_apiserver
    }
}
# 在k8s-master2和k8s-master3分别创建/etc/keepalived/keepalived.conf，注意修改mcast_src_ip和virtual_ipaddress和state 改为BACKUP
# 在k8s-master2节点
$ cat /etc/keepalived/keepalived.conf
! Configuration File for keepalived
global_defs {
    router_id LVS_DEVEL
script_user root
    enable_script_security
}
vrrp_script chk_apiserver {
    script "/etc/keepalived/check_apiserver.sh"
    interval 5
    weight -5
    fall 2
rise 1
}
vrrp_instance VI_1 {
    state BACKUP
    interface eth0
    mcast_src_ip 172.21.51.68
    virtual_router_id 60
    priority 101
    advert_int 2
    authentication {
        auth_type PASS
        auth_pass K8SHA_KA_AUTH
    }
    virtual_ipaddress {
        172.21.51.120
    }
    track_script {
       chk_apiserver
    }
}



#所有master节点配置KeepAlived健康检查文件：
$ cat /etc/keepalived/check_apiserver.sh
#!/bin/bash
err=0
for k in $(seq 1 3)
do
    check_code=$(pgrep haproxy)
    if [[ $check_code == "" ]]; then
        err=$(expr $err + 1)
        sleep 1
        continue
    else
        err=0
        break
    fi
done
if [[ $err != "0" ]]; then
    echo "systemctl stop keepalived"
    /usr/bin/systemctl stop keepalived
    exit 1
else
    exit 0
fi

# 启动haproxy和keepalived---->所有master节点
$ chmod +x /etc/keepalived/check_apiserver.sh
$ systemctl daemon-reload
$ systemctl enable --now haproxy
$ systemctl enable --now keepalived 


# 测试lbip是否生效
$ telnet 172.21.51.120 7443
```

### [3. 初始化配置文件](http://49.7.203.222:2023/#/install/multi-master/init?id=_3-初始化配置文件)

操作节点： 只在k8s-master1节点执行

```yaml
$ cat kubeadm.yaml
apiVersion: kubeadm.k8s.io/v1beta3
bootstrapTokens:
- groups:
  - system:bootstrappers:kubeadm:default-node-token
  token: 7t2weq.bjbawausm0jaxury
  ttl: 24h0m0s
  usages:
  - signing
  - authentication
kind: InitConfiguration
localAPIEndpoint:
  advertiseAddress: 172.21.51.67
  bindPort: 6443
nodeRegistration:
  criSocket: unix:///var/run/containerd/containerd.sock
  imagePullPolicy: IfNotPresent
  name: k8s-master01
  taints:
  - effect: NoSchedule
    key: node-role.kubernetes.io/master
---
apiServer:
  certSANs:
  - 172.21.51.120
  timeoutForControlPlane: 4m0s
apiVersion: kubeadm.k8s.io/v1beta3
certificatesDir: /etc/kubernetes/pki
clusterName: kubernetes
controlPlaneEndpoint: 172.21.51.120:7443
controllerManager: {}
dns:
  type: CoreDNS
etcd:
  local:
    dataDir: /var/lib/etcd
imageRepository: registry.cn-hangzhou.aliyuncs.com/google_containers
kind: ClusterConfiguration
kubernetesVersion: v1.24.4
networking:
  dnsDomain: cluster.local
  podSubnet: 10.244.0.0/16
  serviceSubnet: 10.96.0.0/12
scheduler: {}
```

> 对于上面的资源清单的文档比较杂，要想完整了解上面的资源对象对应的属性，可以查看对应的 godoc 文档，地址: https://godoc.org/k8s.io/kubernetes/cmd/kubeadm/app/apis/kubeadm/v1beta3。

### [4. 提前下载镜像](http://49.7.203.222:2023/#/install/multi-master/init?id=_4-提前下载镜像)

操作节点：所有master节点执行

```python
  # 查看需要使用的镜像列表,若无问题，将得到如下列表
$ kubeadm config images list --config kubeadm.yaml
registry.aliyuncs.com/google_containers/kube-apiserver:v1.24.4
registry.aliyuncs.com/google_containers/kube-controller-manager:v1.24.4
registry.aliyuncs.com/google_containers/kube-scheduler:v1.24.4
registry.aliyuncs.com/google_containers/kube-proxy:v1.24.4
registry.aliyuncs.com/google_containers/pause:3.7
registry.aliyuncs.com/google_containers/etcd:3.5.3-0
registry.aliyuncs.com/google_containers/coredns:v1.8.6

  # 提前下载镜像到本地
$ kubeadm config images pull --config kubeadm.yaml
```

### [5. 初始化master节点](http://49.7.203.222:2023/#/install/multi-master/init?id=_5-初始化master节点)

操作节点：只在k8s-master1节点执行

```bash
$ kubeadm init --config kubeadm.yaml --upload-certs
```

若初始化成功后，最后会提示如下信息：

```bash
...
Your Kubernetes master has initialized successfully!

To start using your cluster, you need to run the following as a regular user:

  mkdir -p $HOME/.kube
  sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
  sudo chown $(id -u):$(id -g) $HOME/.kube/config

You should now deploy a pod network to the cluster.
Run "kubectl apply -f [podnetwork].yaml" with one of the options listed at:
  https://kubernetes.io/docs/concepts/cluster-administration/addons/

Then you can join any number of worker nodes by running the following on each as root:

kubeadm join 172.21.51.120:7443 --token 7t2weq.bjbawausm0jaxury         --discovery-token-ca-cert-hash sha256:b0d875f1dafe9f479b23603c3424cad5e0e3aa0a47a8274f9d24432e97e3dbde         --control-plane --certificate-key 0ea981458813160b6fbc572d415e14cbc28c4bf958a765a7bc989b7ecc5dcdd6
```

接下来按照上述提示信息操作，配置kubectl客户端的认证

```python
  mkdir -p $HOME/.kube
  sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
  sudo chown $(id -u):$(id -g) $HOME/.kube/config
```

> 若执行初始化过程中出错，根据错误信息调整后，执行 kubeadm reset -f ; ipvsadm --clear ; rm -rf ~/.kube

### [6. 添加其他master节点到集群中](http://49.7.203.222:2023/#/install/multi-master/init?id=_6-添加其他master节点到集群中)

```bash
$ kubeadm join 172.21.51.120:7443 --token 7t2weq.bjbawausm0jaxury         --discovery-token-ca-cert-hash sha256:b0d875f1dafe9f479b23603c3424cad5e0e3aa0a47a8274f9d24432e97e3dbde         --control-plane --certificate-key 0ea981458813160b6fbc572d415e14cbc28c4bf958a765a7bc989b7ecc5dcdd6
```

### [7. 添加node节点到集群中](http://49.7.203.222:2023/#/install/multi-master/init?id=_7-添加node节点到集群中)

操作节点：所有的node节点（`k8s-node`）需要执行 在每台node节点，执行如下命令，该命令是在kubeadm init成功后提示信息中打印出来的，需要替换成实际init后打印出的命令。

```python
kubeadm join 172.21.51.120:7443 --token 7t2weq.bjbawausm0jaxury         --discovery-token-ca-cert-hash sha256:b0d875f1dafe9f479b23603c3424cad5e0e3aa0a47a8274f9d24432e97e3dbde      
```

如果忘记添加命令，可以通过如下命令生成：

```bash
$ kubeadm token create --print-join-command
```



## 网络插件

操作节点：只在k8s-master1节点执行

- 下载flannel的yaml文件

  ```bash
  wget https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml
  ```

- 修改配置，指定网卡名称，大概在文件的159行，添加一行配置：

  ```bash
  $ vi kube-flannel.yml
  ...      
  150       containers:
  151       - name: kube-flannel
  152        #image: flannelcni/flannel:v0.19.2 for ppc64le and mips64le (dockerhub limitations may apply)
  153         image: docker.io/rancher/mirrored-flannelcni-flannel:v0.19.2
  154         command:
  155         - /opt/bin/flanneld
  156         args:
  157         - --ip-masq
  158         - --kube-subnet-mgr
  159         - --iface=eth0   # 如果机器存在多网卡的话，指定内网网卡的名称，默认不指定的话会找第一块网卡
  160         resources:
  161           requests:
  162             cpu: "100m"
  163             memory: "50Mi"
  ...
  ```

- 确认pod网段

  ```bash
  vi kube-flannel.yml
   82   net-conf.json: |
   83     {
   84       "Network": "10.244.0.0/16",
   85       "Backend": {
   86         "Type": "vxlan"
   87       }
   88     }
   
  # 确认84行的网段和前面kubeadm.yaml中初始化使用的配置中的podSubnet保持一致！
  ```

- 执行安装flannel网络插件

  ```bash
  # 执行flannel安装
  kubectl apply -f kube-flannel.yml
  kubectl -n kube-flannel get po -owide
  ```



## 集群设置

### [设置master节点是否可调度（可选）](http://49.7.203.222:2023/#/install/multi-master/cluster-setting?id=设置master节点是否可调度（可选）)

操作节点：`k8s-master`

默认部署成功后，master节点无法调度业务pod，如需设置master节点也可以参与pod的调度，需执行：

```bash
kubectl taint node k8s-master node-role.kubernetes.io/master:NoSchedule-
kubectl taint node k8s-master node-role.kubernetes.io/control-plane:NoSchedule-
```

> 课程后期会部署系统组件到master节点，因此，此处建议设置k8s-master节点为可调度

### [设置kubectl自动补全](http://49.7.203.222:2023/#/install/multi-master/cluster-setting?id=设置kubectl自动补全)

操作节点：`k8s-master`

```bash
$ yum install bash-completion -y
$ source /usr/share/bash-completion/bash_completion
$ source <(kubectl completion bash)
$ echo "source <(kubectl completion bash)" >> ~/.bashrc
```



## 调整证书过期

使用kubeadm安装的集群，证书默认有效期为1年，可以通过如下方式修改为10年。

```bash
cd /etc/kubernetes/pki

# 查看当前证书有效期
for i in $(ls *.crt); do echo "===== $i ====="; openssl x509 -in $i -text -noout | grep -A 3 'Validity' ; done

mkdir backup_key; cp -rp ./* backup_key/
git clone https://github.com/yuyicai/update-kube-cert.git
cd update-kube-cert/ 
bash update-kubeadm-cert.sh all

#若无法clone项目，可以手动在浏览器中打开后，复制update-kubeadm-cert.sh 脚本内容到机器中执行

```



## 验证集群

操作节点： 在master节点（`k8s-master`）执行

```python
$ kubectl get nodes  #观察集群节点是否全部Ready
```

创建测试nginx服务

```python
$ kubectl run  test-nginx --image=nginx:alpine
```

查看pod是否创建成功，并访问pod ip测试是否可用

```bash
$ kubectl get po -o wide
NAME                          READY   STATUS    RESTARTS   AGE   IP           NODE         NOMINATED NODE   READINESS GATES
test-nginx-5bd8859b98-5nnnw   1/1     Running   0          9s    10.244.1.2   k8s-slave1   <none>           <none>
$ curl 10.244.1.2
...
<h1>Welcome to nginx!</h1>
<p>If you see this page, the nginx web server is successfully installed and
working. Further configuration is required.</p>

<p>For online documentation and support please refer to
<a href="http://nginx.org/">nginx.org</a>.<br/>
Commercial support is available at
<a href="http://nginx.com/">nginx.com</a>.</p>

<p><em>Thank you for using nginx.</em></p>
</body>
</html>
```



## containerd客户端介绍

操作节点：所有节点

由于新版本的k8s直接采用`containerd`作为容器运行时，因此，后续创建的服务，通过`docker`的命令无法查询，因此，如果有需要对节点中的容器进行操作的需求，需要用`containerd`的命令行工具来替换，目前总共有三种，包含：

- ctr
- crictl
- nerctl

###### [ctr](http://49.7.203.222:2023/#/install/multi-master/containerd-cli?id=ctr)

ctr为最基础的`containerd`的操作命令行工具，安装`containerd`时已默认安装，因此无需再单独安装。

ctr的可操作的命令很少，且很不人性化，因此极力不推荐使用

Containerd 也有 namespaces 的概念，对于上层编排系统的支持，`ctr` 客户端 主要区分了 3 个命名空间分别是`k8s.io`、`moby`和`default`

比如操作容器和镜像：

```bash
# 查看containerd的命名空间
ctr ns ls;

# 查看containerd启动的容器列表
ctr -n k8s.io container ls

# 查看镜像列表
ctrl -n k8s.io image ls

# 导入镜像
ctr -n=k8s.io image import dashboard.tar

# 从私有仓库拉取镜像，前提是/etc/containerd/certs.d下已经配置过该私有仓库的非安全认证
ctr images pull --user admin:admin  --hosts-dir "/etc/containerd/certs.d"  172.21.65.226:5000/eladmin/eladmin-api:v1-rc1

# ctr命令无法查看容器的日志，也无法执行exec等操作
```

###### [crictl](http://49.7.203.222:2023/#/install/multi-master/containerd-cli?id=crictl)

`crictl` 是遵循 CRI 接口规范的一个命令行工具，通常用它来检查和管理kubelet节点上的容器运行时和镜像。

主机安装了 k8s 后，命令行会有` crictl` 命令，无需单独安装。

`crictl` 命令默认使用`k8s.io` 这个名称空间，因此无需单独指定，使用前，需要先加一下配置文件：

```bash
cat /etc/crictl.yaml
runtime-endpoint: unix:///run/containerd/containerd.sock
image-endpoint: unix:///run/containerd/containerd.sock
timeout: 10
debug: false
```

常用操作：

```bash
# 查看容器列表
crictl ps

# 查看镜像列表
crictl images 

# 删除镜像
crictl rmi 172.21.51.67:5000/eladmin/eladmin-api:v1-rc1

# 拉取镜像， 若拉取私有镜像，需要修改containerd配置添加认证信息，比较麻烦且不安全
crictl pull nginx:alpine

# 执行exec操作
crictl ps 
CONTAINER           IMAGE               CREATED             STATE               NAME                      ATTEMPT             POD ID              POD
d23fe516d2eeb       8b0e63fd4fec6       5 hours ago         Running             eladmin-api               0                   5dbae572dcb6b       eladmin-api-5d979bb778-tc5kz

# 注意只能使用containerid
crictl exec -ti d23fe516d2eeb bash

# 查看容器日志
crictl logs -f d23fe516d2eeb

# 清理镜像
crictl rmi --prune
```

###### [nerdctl](http://49.7.203.222:2023/#/install/multi-master/containerd-cli?id=nerdctl)

推荐使用 `nerdctl`，使用效果与 docker 命令的语法基本一致 , 官网`https://github.com/containerd/nerdctl`

安装：

```bash
# 下载精简版安装包，精简版的包无法使用nerdctl进行构建镜像
wget https://github.com/containerd/nerdctl/releases/download/v0.23.0/nerdctl-0.23.0-linux-amd64.tar.gz

#如果下载超时或者速度慢，也可以去网盘自取
链接: https://pan.baidu.com/s/14Q2tPbiNXdN-PLKk1hpKhA 提取码: 496v 

# 解压后，将nerdctl 命令拷贝至$PATH下即可
cp nerdctl /usr/bin/
```

常用操作：

```bash
# 查看镜像列表
nerdctl -n k8s.io ps -a

# 执行exec
nerdctl -n k8s.io exec -ti e2cd02190005 sh

# 登录镜像仓库
nerdctl login 172.21.51.67:5000

# 拉取镜像,如果是想拉取了让k8s使用，一定加上-n k8s.io,否则会拉取到default空间中， k8s默认只使用k8s.io
nerdctl -n k8s.io pull 172.21.51.67:5000/eladmin/eladmin-api:v1-rc1


# 启动容器
nerdctl -n k8s.io run -d --name test nginx:alpine

# exec
nerdctl -n k8s.io  exec -ti test sh

# 查看日志, 注意，nerdctl 只能查看使用nerdctl命令创建从容器的日志，k8s中kubelet创建的产生的容器无法查看
nerdctl -n k8s.io logs -f test

# 构建，但是需要额外安装buildkit的包
nerdctl build . -t xxxx:tag -f Dockerfile
```

###### [使用小经验](http://49.7.203.222:2023/#/install/multi-master/containerd-cli?id=使用小经验)

- 用了k8s后，对于业务应用的基本操作，90%以上都可以通过`kubectl`命令行完成
- 对于镜像的构建，仍然推荐使用`docker build` 来完成，推送到镜像仓库后，containerd可以直接使用
- 对于查看containerd中容器的日志，使用 `crictl logs`完成，因为ctr、nerdctl均不支持
- 对于其他常规的containerd容器操作，建议使用nerdctl完成

更多命令可以参考下文：

- https://www.modb.pro/db/485911
- https://github.com/containerd/nerdctl#container-management



## [部署dashboard](http://49.7.203.222:2023/#/install/multi-master/dashboard?id=部署dashboard)

- 部署服务

```bash
# 推荐使用下面这种方式
$ wget https://raw.githubusercontent.com/kubernetes/dashboard/v2.2.0/aio/deploy/recommended.yaml
$ vi recommended.yaml
# 修改Service为NodePort类型，文件的45行上下
......
kind: Service
apiVersion: v1
metadata:
  labels:
    k8s-app: kubernetes-dashboard
  name: kubernetes-dashboard
  namespace: kubernetes-dashboard
spec:
  ports:
    - port: 443
      targetPort: 8443
  selector:
    k8s-app: kubernetes-dashboard
  type: NodePort  # 加上type=NodePort变成NodePort类型的服务
......
```

- 查看访问地址，本例为30133端口

```bash
$ kubectl apply -f recommended.yaml
$ kubectl -n kubernetes-dashboard get svc
NAME                        TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)         AGE
dashboard-metrics-scraper   ClusterIP   10.105.62.124   <none>        8000/TCP        31m
kubernetes-dashboard        NodePort    10.103.74.46    <none>        443:30133/TCP   31m 
```

- 使用浏览器访问 [https://172.21.51.143:30133，其中172.21.51.143为master节点的外网ip地址，chrome目前由于安全限制，默认访问受限制，在chrome浏览器页面点击任意空白处，直接键盘输入“thisisunsafe”即可进行访问。](https://172.21.51.143:30133，其中172.21.51.143为master节点的外网ip地址，chrome目前由于安全限制，默认访问受限制，在chrome浏览器页面点击任意空白处，直接键盘输入“thisisunsafe”即可进行访问。/)
- 创建ServiceAccount进行访问

```bash
$ vi dashboard-admin.conf
kind: ClusterRoleBinding
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: admin
  annotations:
    rbac.authorization.kubernetes.io/autoupdate: "true"
roleRef:
  kind: ClusterRole
  name: cluster-admin
  apiGroup: rbac.authorization.k8s.io
subjects:
- kind: ServiceAccount
  name: admin
  namespace: kubernetes-dashboard

---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: admin
  namespace: kubernetes-dashboard

$ kubectl apply -f dashboard-admin.conf
# 创建访问token
$ kubectl -n kubernetes-dashboard create token admin
eyJhbGciOiJSUzI1NiIsImtpZCI6Ik1rb2xHWHMwbWFPMjJaRzhleGRqaExnVi1BLVNRc2txaEhETmVpRzlDeDQifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlcm5ldGVzLWRhc2hib2FyZCIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJhZG1pbi10b2tlbi1mcWRwZiIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50Lm5hbWUiOiJhZG1pbiIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6IjYyNWMxNjJlLTQ1ZG...
```

![img](2Kubernetes安装文档.assets/dashboard-166903877809361.png)

![img](2Kubernetes安装文档.assets/dashboard-content-166903877809362.jpg)



## 清理集群

如果你的集群安装过程中遇到了其他问题，我们可以使用下面的命令来进行重置：

```bash
# 在全部集群节点执行
kubeadm reset
ifconfig cni0 down && ip link delete cni0
ifconfig flannel.1 down && ip link delete flannel.1
rm -rf /run/flannel/subnet.env
rm -rf /var/lib/cni/
mv /etc/kubernetes/ /tmp
mv /var/lib/etcd /tmp
mv ~/.kube /tmp
iptables -F
iptables -t nat -F
ipvsadm -C
ip link del kube-ipvs0
ip link del dummy0
```
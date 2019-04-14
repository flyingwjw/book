## 环境准备

1.  关闭自带的防火墙服务

```
# systemctl disable firewalld
# systemctl stop firwalld
```

2. 安装etcd和Kubernetes软件（会自动安装Docker软件）

```
# yum install -y etcd kubernetes
```

3. 修改配置文件

* Docker配置文件/etc/sysconfig/docker

OPTIONS='--selinux-enabled=false --insecure-registry gcr.io'

* Kubernetes apiserver配置文件/etc/kubernetes/apiserver,把--admission_control
参数中的ServiceAccount删除

4. 按顺序启动服务

```
# systemctl start etcd
# systemctl start docker
# systemctl start kube-apiserver
# systemctl start kube-controller-manager
# systemctl start kube-scheduler
# systemctl start kubelet
# systemctl start kube-proxy
```
设置为开机自启动

```
# systemctl enable etcd
# systemctl enable docker
# systemctl enable kube-apiserver
# systemctl enable kube-controller-manager
# systemctl enable kube-scheduler
# systemctl enable kubelet
# systemctl enable kube-proxy
```



## 启动 MySQL服务

为MySQL服务创建RC定义文件: **mysql-rc.yaml**

```
apiVersion: v1
kind: ReplicationController
metadata:
  name: mysql
spec:
  replicas: 1
  selector:
    app: mysql
  template:
    metadata:
      labels:
        app: mysql
    spec:
      containers:
      - name: mysql
        image: mysql
        ports:
        - containerPort: 3306
        env:
        - name: MYSQL_ROOT_PASSWORD
          value: "123456"
```

发布到Kubernetes集群，在Master节点执行命令：

```
$ kubectl create -f mysql-rc.yaml
```

查看RC，Pod

```
$ kubectl get rc
$ kubectl get pods
```

创建与之关联的Kubernetes Service MySQL定义文件：mysql-svc.yaml

```
apiVersion: v1
kind: Service
metadata:
  name: mysql
spec:
  ports:
    - port: 3306
  selector:
    app: mysql
```
发布到Kubernetes集群，在Master节点执行命令：

```
$ kubectl create -f mysql-svc.yaml
```

查看RC，Pod

```
$ kubectl get svc
```

* 问题1：使用k8s创建容器一直处于ContainerCreating状态

```
$ kubectl describe pods mysql

Name:		mysql-pj4vz
Namespace:	default
Node:		127.0.0.1/127.0.0.1
Start Time:	Wed, 03 Apr 2019 00:34:22 +0800
Labels:		app=mysql
Status:		Pending
IP:		
Controllers:	ReplicationController/mysql
Containers:
  mysql:
    Container ID:	
    Image:		mysql
    Image ID:		
    Port:		3306/TCP
    State:		Waiting
      Reason:		ContainerCreating
    Ready:		False
    Restart Count:	0
    Volume Mounts:	<none>
    Environment Variables:
      MYSQL_ROOT_PASSWORD:	123456
Conditions:
  Type		Status
  Initialized 	True 
  Ready 	False 
  PodScheduled 	True 
No volumes.
QoS Class:	BestEffort
Tolerations:	<none>
Events:
  FirstSeen	LastSeen	Count	From			SubObjectPath	Type		Reason		Message
  ---------	--------	-----	----			-------------	--------	------		-------
  19m		19m		1	{default-scheduler }			Normal		Scheduled	Successfully assigned mysql-pj4vz to 127.0.0.1
  19m		3m		8	{kubelet 127.0.0.1}			Warning		FailedSync	Error syncing pod, skipping: failed to "StartContainer" for "POD" with ErrImagePull: "image pull failed for registry.access.redhat.com/rhel7/pod-infrastructure:latest, this may be because there are no credentials on this request.  details: (open /etc/docker/certs.d/registry.access.redhat.com/redhat-ca.crt: no such file or directory)"

  18m	8s	80	{kubelet 127.0.0.1}		Warning	FailedSync	Error syncing pod, skipping: failed to "StartContainer" for "POD" with ImagePullBackOff: "Back-off pulling image \"registry.access.redhat.com/rhel7/pod-infrastructure:latest\""
```

解决方法：
```
$ wget http://mirror.centos.org/centos/7/os/x86_64/Packages/python-rhsm-certificates-1.19.10-1.el7_4.x86_64.rpm
$ rpm2cpio python-rhsm-certificates-1.19.10-1.el7_4.x86_64.rpm | cpio -iv --to-stdout | tee ./redhat-uep.pem
$ sudo mv ./redhat-uep.pem /etc/rhsm/ca/redhat-uep.pem
$ docker pull registry.access.redhat.com/rhel7/pod-infrastructure:latest
```

##  启动Tomcat应用

RC文件：myweb-rc.yaml

```
apiVersion: v1
kind: ReplicationController
metadata:
  name: myweb
spec:
  replicas: 5
  selector:
    app: myweb
  template:
    metadata:
      labels:
        app: myweb
    spec:
      containers:
        - name: myweb
          image: kubeguide/tomcat-app:v1
          ports:
          - containerPort: 8080
          env:
          - name: MYSQL_SERVICE_HOST
            value: 'mysql'
          - name: MYSQL_SERVICE_PORT
            value: '3306'
```

SVC文件 myweb-svc.yaml ：

```
apiVersion: v1
kind: Service
metadata:
  name: myweb
spec:
  type: NodePort
  ports:
    - port: 8080
      nodePort: 30001
  selector:
    app: myweb
```

命令

```
$ kubectl create -f myweb-rc.yaml
$ kubectl create -f myweb-svc.yaml
```




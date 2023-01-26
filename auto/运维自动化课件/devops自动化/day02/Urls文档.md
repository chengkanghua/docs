# 六 代码发布

在接下来的学习中，我们要在我们的运维平台上添加代码发布功能，实际上就是要实现一套自动化项目构建与部署方案。



## 发布方案

### 传统代码发布

![image-20210106153814329](assets/image-20210106153814329.png)



+ 开发者开发代码，开发完毕后将代码打包，提交给运维人员Ops
+ 运维人员获取包，手工将包部署到对应的环境Env当中
+ 运维人员部署完毕后，通知测试人员环境部署完毕
+ 测试人员开始进行测试，测试对应功能是否正确，进行缺陷管理
+ 测试完毕后若有Bug，开发进行修复，修复后则重新开始进行步骤1的操作
+ 所以缺陷修复并测试通过后，项目发布上线

在这个过程当中，开发团队开发编码，打包提交，但没有以常规、可重复的方式安装/部署产品。因此在整个周期中，安装/部署任务（以及其它支持任务）就会留给了运维团队来负责，而运维人员部署完成以后才通知测试人员进行测试，这经常导致很多混乱和问题，因为运维团队在后期才开始介入，并且必须在短时间内完成工作。同样开发团队也会因为这种模式而经常处于不利地位 （因为开发人员没有充分测试产品的安装/部署功能），这往往导致开发团队和运维团队、测试团队之间严重脱节和缺乏合作。



这种情况在中国开发行业中持续了很久，直到2006年，在中国软件产业发展高峰论坛上迎来了一位便捷开发布道师——[**Martin Fowler（马丁·福勒）**](https://baike.baidu.com/item/%E9%A9%AC%E4%B8%81%C2%B7%E7%A6%8F%E5%8B%92/3107032)，他在发表演讲时提到了一个让人无法理解的事情：“原本为期需要8个月构建交付的项目，只需要两个月时就已经上线，并开始向客户收钱了。”，以此把敏捷开发的最佳实现方案-持续集成这个概念引入了中国。

![img](assets/bg2015092301.png)

**持续集成指的是，频繁地（一天多次）将代码集成到主干。**

> **持续集成好处主要有两点：
>
> （1）快速发现错误。每完成一点更新，就集成到主干，可以快速发现错误，定位错误也比较容易。
>
> （2）防止分支大幅偏离主干。如果不是经常集成，主干又在不断更新，会导致以后集成的难度变大，甚至难以集成。**集成地狱**

**持续集成的目的，就是让产品可以快速迭代，同时还能保持高质量。**它的核心措施是，代码集成到主干之前，必须通过自动化测试，自动化部署。只要有一个测试用例失败，就不能集成。

Martin Fowler说过，"持续集成并不能消除Bug，而是让它们非常容易发现和改正。"



### 自动化部署-CI/CD

CI/CD 的核心概念是持续集成（Continuous Integration）、持续交付（Continuous Delivery）与持续部署（Continuous Deployment），它实现了从开发、编译、测试、发布、部署自动化的一套自动化构建的流程。



![cicd](assets/cicd.png)



持续集成（CI）是在源代码变更后自动检测、拉取、构建和（在大多数情况下）进行单元测试的过程，持续集成的目标是**快速确保开发人员新提交的变更是好的，并且适合在代码库中进一步使用**。持续集成的基本思想是让一个自动化过程监测一个或多个源代码仓库是否有变更。当变更被推送到仓库时，它会监测到更改、下载副本、构建并运行任何相关的单元测试。

监测程序通常是像 [Jenkins](https://jenkins.io/) 这样的应用程序，它还协调管道中运行的所有（或大多数）进程，监视变更是其功能之一。监测程序可以以几种不同方式监测变更。这些包括：

- **轮询**：监测程序反复询问代码管理系统，当代码管理系统有新的变更时，监测程序会“唤醒”并完成其工作以获取新代码并构建/测试它。
- **定期**：监测程序配置为定期启动构建，无论源码是否有变更。理想情况下，如果没有变更，则不会构建任何新内容，因此这不会增加额外的成本。
- **推送**：这与用于代码管理系统检查的监测程序相反。在这种情况下，代码管理系统被配置为提交变更到仓库时将“推送”一个通知到监测程序。最常见的是，这可以以 webhook 的形式完成 —— 在新代码被推送时一个挂勾hook的程序通过互联网向监测程序发送通知。为此，监测程序必须具有可以通过网络接收 webhook 信息的开放端口。

持续交付（CD）通常是指整个流程链（管道），它自动监测源代码变更并通过构建、测试、打包和相关操作运行它们以生成可部署的版本，基本上没有任何人为干预。持续交付的目标是**自动化、效率、可靠性、可重复性和质量保障（通过持续测试CT）**，持续交付包含持续集成（自动检测源代码变更、执行构建过程、运行单元测试以验证变更），持续测试（对代码运行各种测试以保障代码质量），和（可选）持续部署（通过管道发布版本自动提供给用户）。



持续部署（CD）是指能够自动提供持续交付管道中发布版本给最终用户使用的想法。根据用户的安装方式，可能是在云环境中自动部署、app 升级（如手机上的应用程序）、更新网站或只更新可用版本列表。





## CI/CD部署流程

![image-20220807073549938](assets/image-20220807073549938.png)



实现效果图：

所谓的应用，实际上代表的就是我们要远程发布的代码的项目版本或者项目中的一个功能代码版本。

![image-20220807074304367](assets/image-20220807074304367.png)



![image-20220807074318784](assets/image-20220807074318784.png)



配置部署的环境与Git仓库地址，同时设置是否在发布成功或事变时设置结果通知。

![image-20220807074341917](assets/image-20220807074341917.png)



由于我们进行代码发布的时候，需要选择环境(测试环境、运营环境等等)，来区分我们本次将代码发布到什么环境的主机。

![image-20210120142752339](assets/image-20210120142752339.png)



环境是针对公司内部的资产根据实际业务进行再次划分的单位。会存在1个服务器，在不同的时间属于多个不同的环境，一个环境有可能配套了多个企业资产。

![image-20210120142832689](assets/image-20210120142832689.png)



## 软件安装

### jetkins

官网地址：https://www.jenkins.io/zh/

安装文档：https://www.jenkins.io/zh/doc/book/installing/



#### 系统要求

最低推荐配置:

- 256MB可用内存（JVM）
- 1GB可用磁盘空间(作为一个[Docker](https://www.jenkins.io/zh/doc/book/installing/#docker)容器运行jenkins的话推荐10GB)

为小团队推荐的硬件配置：

- 1GB+可用内存
- 50 GB+ 可用磁盘空间

软件配置:

- Java 8—无论是Java运行时环境（JRE）还是Java开发工具包（JDK）都可以。

**注意:** 如果将Jenkins作为Docker 容器运行，这不是必需的。



#### 版本说明

jenkins实际上由2个发布版本，分别是：**LTS**（长期支持版本）与 **Weekly**（普通发行版本）。

| 版本号          | 描述                                                         |
| --------------- | ------------------------------------------------------------ |
| 稳定版 (LTS)    | LTS (长期支持) 版本每12周从常规版本流中选择，作为该时间段的稳定版本。<br> 每隔 4 周，我们会发布稳定版本，其中包括错误和安全修复反向移植。 |
| 定期发布 (每周) | 每周都会发布一个新版本，为用户和插件开发人员提供错误修复和功能。 |

这里，我们直接开发使用 稳定版 (LTS) 。



#### 安装

docker-compose安装jetkins，docker-compose.yaml，代码：

```yaml
version: '3.7'
services:
  jenkins:
    image: 'jenkins/jenkins:lts-jdk11'
    container_name: jenkins
    restart: always
    user: root
    environment:
      - TZ=Asia/Shanghai
    ports:
      - '8888:8080'
      - '5000:50000'
    volumes:
      - './data/jenkins:/var/jenkins_home'
```

注释版：

```yaml
version: '3.7'   # docker-compose版本，目前最新版本是3.9版本，此处我们使用3.7即可。
services:          # 容器服务列表，一个docker-complse.yaml文件中只能有一个services
  jenkins:         # 服务名
    image: 'jenkins/jenkins:lts-jdk11'   # 当前容器的基础镜像
    container_name: jenkins   # 容器名
    restart: always                   # 设置开机自启，注意：如果公司安装的不是docker，而是podman的话。podman是没有这个配置的，如果要设置容器开机自启，只能借助python的supervisor这样的进程管理器来启动。
    user: root                          # 以root用户身份启动容器
    environment:                    # 容器内系统环境变量。
      - TZ=Asia/Shanghai       # 设置时区和国际化本地化
    ports:                                # 容器内部与宿主机之间的端口映射： 宿主机端口:容器端口
      - '8888:8080'
      - '5000:50000'                # 如果是windows下使用docker-desktop要调整50000端口为其他端口，因为50000被windows虚拟机hyper-V占用了。linux或macOS没这个问题
    volumes:                          # 逻辑卷配置，设置目录映射：宿主机路径: 容器内部路径
      - './data/jenkins:/var/jenkins_home'
```

拉取镜像启动docker容器（注意：要保证当前开发电脑上已经安装了docker、docker-compose，docker-compose依赖于python环境）。

```bash
# cd 项目根目录下，创建上面的 docker-compose.yaml
docker-compose up -d

# 如果要关闭当前docker-compose.yaml中所有的容器服务，则可以使用
docker-compose down

# 如果要查看某个容器运行过程中的日志
docker logs <容器名>
# 监控容器的日志
docker logs -f <容器名>
```



安装完成以后，等待2分钟左右，可以通过浏览器访问`http://127.0.0.1:8888`(如果你设置的也是这个端口的话)访问jenkins的管理站点。效果如下：

![image-20220807082912490](assets/image-20220807082912490.png)

按界面中所说，进入找到容器内部`/var/jenkins_home`目录的映射路径`./data/jenkins`目录下的初始化密码文件复制密码，点击"继续"。

![image-20220807083048843](assets/image-20220807083048843.png)

登陆后续界面如下：

![image-20220807083133927](assets/image-20220807083133927.png)



建议选择“安装推荐的插件”，若插件安装失败，多试几次即可)，当然，也可以选择右边的自定义插件安装，先选择不安装插件，先进去也可以。

![image-20220807083321579](assets/image-20220807083321579.png)



插件下载较慢是由于插件源服务器在国外，可以根据以下教程切换插件源服务器地址改成国内的。

当然也可以一直重试到下载完成为止。

>更换为国内插件源
>
>**方式1：**
>
>选择右边的自定义插件安装，先选择不安装插件，在配置管理员账号进入到jenkins管理页面时，点击"Manage Jenkins"--->"Manage Plugins"--->"Advanced"
>
>![image-20220807085603818](assets/image-20220807085603818.png)
>
>将上图的URL地址改为清华源并点击提交即可：https://mirrors.tuna.tsinghua.edu.cn/jenkins/updates/update-center.json
>
>**方式2：**
>
>更改配置文件（`jenkins_home/updates/default.json`），我们现在的jenkins应用安装在docker并做了数据映射，因此直接在宿主机下进行修改即可。
>
>![image-20220807083657800](assets/image-20220807083657800.png)
>
>因为default.json配置文件配置内容较多，修改的地址也很多，因此建议使用代码编辑器替换（Ctrl+H/Ctrl+R）或者`使用sed命令`进行替换：
>
>sed -i 's#https://updates.jenkins.io/download#https://mirrors.tuna.tsinghua.edu.cn/jenkins#g' default.json && sed -i 's#http://www.google.com#https://www.baidu.com#g' default.json
>
>完成以后，重启jenkins即可。

安装完成以后，创建管理员。

>注意：
>
>老师不知道各位同学的密码！！！自己设置的麻烦自己记一下哈。

![image-20220807084628321](assets/image-20220807084628321.png)



实例配置，默认点击继续即可。

![image-20220807084730598](assets/image-20220807084730598.png)

配置完成！

![image-20220807084811373](assets/image-20220807084811373.png)



进入主界面，以后登陆的界面如下：

![image-20220807084852131](assets/image-20220807084852131.png)

在前面如果没有选择安装推荐的插件，而是选择自定义安装而没有安装插件的同学，可以`系统管理`->`插件管理`处，进行插件的安装与卸载操作。常用的插件：git、pipeline、Blue Ocean、Allure等等。

![image-20220807085250252](assets/image-20220807085250252.png)



#### 基本使用

接下来，我们快速使用jenkins来完成一个工程（就是一个项目的CI构建流程）。

![image-20220807090418130](assets/image-20220807090418130.png)



填写任务名称，并勾选默认插件，此处我们选择第一个"freestyle project"。

![image-20220807090338851](assets/image-20220807090338851.png)

上面的操作项目于创建了一个项目工程的发布流程。

![image-20220807091007792](assets/image-20220807091007792.png)

![image-20220807091038299](assets/image-20220807091038299.png)

![image-20220807121659671](assets/image-20220807121659671.png)

![image-20220807091122735](assets/image-20220807091122735.png)

保存成功以后，可以在demo工程的管理菜单左侧选择立即构建。

![image-20220807091439271](assets/image-20220807091439271.png)

等待以后，可以点击查看构建历史：

![image-20220807091618526](assets/image-20220807091618526.png)



查看构建过程中的控制台输出。

![image-20220807092156936](assets/image-20220807092156936.png)



#### 系统配置

##### 中文支持

默认是没有该配置的，需要安装额外安装中文扩展插件。安装中文扩展，等待jenkins重启。

![image-20220807131812612](assets/image-20220807131812612.png)



重启完成以后，如果出现部分页面翻译一半的情况，可以打开系统设置，找到Locale选项，设置中文，接着访问http://127.0.0.1:8888/restart进行重启。

![image-20220807131336782](assets/image-20220807131336782.png)



##### 凭据管理

所谓的凭据就是当前jenkins所在服务器对远程服务器节点进行操作的登陆凭证（可以是账号密码，也可以是sshkey）

![image-20220807134639184](assets/image-20220807134639184.png)

![image-20220807134741857](assets/image-20220807134741857.png)



![image-20220807134803406](assets/image-20220807134803406.png)



![image-20220807134716272](assets/image-20220807134716272.png)



![image-20220807140324269](assets/image-20220807140324269.png)



##### 节点管理

节点（node），实际上就是jenkins用于在分布式主机下执行构建任务的服务器。

点击进入节点管理功能。

![image-20220807124932584](assets/image-20220807124932584.png)



右侧是节点名称。点击左侧红框位置可以新建节点。

![image-20220807125019994](assets/image-20220807125019994.png)



节点名称，可以自定义的名称，但最好将远程服务器的ip地址或者计算机名填上，便于后期维护查看。

![image-20220807135123438](assets/image-20220807135123438.png)



节点连接配置

![image-20220807135526068](assets/image-20220807135526068.png)

![image-20220807135555097](assets/image-20220807135555097.png)

在节点对应的服务器上，使用`which git`，可以查看git命令的路径位置。

使用`echo $JAVE_HOME`，可以查看java的工作目录。

![image-20220807135627721](assets/image-20220807135627721.png)

完成上面配置以后，点击"保存"。

并在新建节点对应的服务器（也就是上面添加的192.168.233.129）修改jenkins工作目录的权限并为jenkins设置java链接文件。

```bash
# 这里 /var/jenkins/workspace 为上述步骤设置的节点的工作目录
sudo mkdir -p /var/jenkins/workspace/jdk/bin/

sudo chown -P moluo:moluo /var/jenkins

which java
#  which java 命令的结果，/usr/bin/java，然后创建软连接
sudo ln -s /usr/bin/java /var/jenkins/workspace/jdk/bin/java
```

节点配置成功。

![image-20220807140655654](assets/image-20220807140655654.png)



#### 用户管理

在jenkins安装完成以后，默认需要创建了一个超级管理员。但是在企业开发中，肯定不是所有人都使用超管账号的，而且不同的团队人员，能使用jenkins的功能权限应该也是不一样的。所以需要进行用户的账号分配以及权限分配。

从系统配置中点击全局安全配置，设置开启用户管理。

![image-20220807154517945](assets/image-20220807154517945.png)

![image-20220807154838325](assets/image-20220807154838325.png)

点击进入用户管理功能。

![image-20220807154903279](assets/image-20220807154903279.png)

点击"新建用户"

![image-20220807141107679](assets/image-20220807141107679.png)



删除用户。

![image-20220807155042377](assets/image-20220807155042377.png)

指定用户分配权限。

![image-20220807155650655](assets/image-20220807155650655.png)



#### 通知配置

jenkins在构建任务完成以后，可以设置结果通知的。它支持邮件通知、企业微信、钉钉等等，但是都需要安装插件才可以使用。

这里，我们使用邮件通知看下jenkins的通知效果。



##### 安装插件

进入系统管理->插件管理->可选插件，安装Email Extension Template、Email Extension Plugin和Build Timestamp插件

![image-20220807142414119](assets/image-20220807142414119.png)

安装等待jenkins重启。



在系统配置->设置邮件发送人的邮箱地址。

![image-20220807160901504](assets/image-20220807160901504.png)

开启构建任务完成以后的邮件发送规则。

![image-20220807161131228](assets/image-20220807161131228.png)

![image-20220807161216460](assets/image-20220807161216460.png)



配置邮件通知。

登陆要使用的SMTP服务器所在的站点配置，设置第三方邮件发送服务。

SMTP（简单邮件发送协议，Simple Mail Transfer Protocol）服务器，就是邮件服务器所在的网关地址。

![image-20220807162422697](assets/image-20220807162422697.png)



![image-20220807162717648](assets/image-20220807162717648.png)

![image-20220807162801728](assets/image-20220807162801728.png)

完成上面配置以后，可以通过点击"**通过发送测试邮件测试配置**"进行发送测试邮件，验证上面的配置是否正确！

![image-20220807163107584](assets/image-20220807163107584.png)



##### 配置邮件模板内容

进入系统管理 - 系统配置，配置获取的时间戳格式 用于发送邮件时获取log和html报告为邮件附件
![在这里插入图片描述](assets/2c2587e607d548bc91638bd394a33531.png)



配置发送邮件账号与邮件类型
![在这里插入图片描述](assets/e77ff665c5a64328ba098b390b012f41.png)



设置默认收件、邮件标题和邮件内容
![在这里插入图片描述](assets/103e9096af9645b4994225c28c58df84.png)

jenkins提供的邮件发送变量

| 变量名        | 描述                        |
| ------------- | --------------------------- |
| $PROJECT_NAME | 构建任务的项目名（job名称） |
| $BUILD_NUMBER | 构建任务的编号ID            |
| $BUILD_STATUS | 构建任务的结果              |
| $CAUSE        | 构建任务的失败原因          |
| $PROJECT_URL  | 构建任务的详情URL地址       |

default content（默认邮件模板）：

```html
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>${PROJECT_NAME}-第${BUILD_NUMBER}次构建日志</title>
</head>
<body leftmargin="8" marginwidth="0" topmargin="8" marginheight="4" offset="0">
    <table width="95%" cellpadding="0" cellspacing="0"  style="font-size: 11pt; font-family: Tahoma, Arial, Helvetica, sans-serif">
        <tr>本邮件由jenkins系统自动发出，无需回复，以下为${PROJECT_NAME }项目构建信息</br>
            <td><font color="#CC0000">构建结果 - ${BUILD_STATUS}</font></td>
        </tr>
        <tr>
            <td><br />
            <b><font color="#0B610B">构建信息</font></b>
            <hr size="2" width="100%" align="center" /></td>
        </tr>
        <tr>
            <td>
                <ul>
                    <li>项目名称：${PROJECT_NAME}</li>
                    <li>构建编号：第${BUILD_NUMBER}次构建</li>
                    <li>触发原因：${CAUSE}</li>
                    <li>构建状态：${BUILD_STATUS}</li>
                    <li>项目URL：<a href="${PROJECT_URL}">${PROJECT_URL}</a></li>
                    <li>工作目录：<a href="${PROJECT_URL}ws">${PROJECT_URL}ws</a></li>
                    <li>构建URL：<a href="${BUILD_URL}">${BUILD_URL}</a></li>
                    <li>构建日志： <a href="${BUILD_URL}console">${BUILD_URL}console</a></li>
                    <li>测试报告：<a href="${BUILD_URL}HTML_20Report/">${BUILD_URL}HTML_20Report/</a></li>
                </ul>
                <h4><font color="#0B610B">失败用例</font></h4>
                <hr size="2" width="100%" />$FAILED_TESTS<br/>
                <h4><font color="#0B610B">最近提交版本(git：$GIT_REVISION)</font></h4>
                <hr size="2" width="100%" />
                <ul>
                ${CHANGES_SINCE_LAST_SUCCESS, reverse=true, format="%c", changesFormat="<li>%d[%a] %m</li>"}
                </ul>
                    详细提交: <a href="${PROJECT_URL}changes">${PROJECT_URL}changes</a><br/>
            </td>
        </tr>
    </table>
</body>
</html>
```



Default Triggers（发送邮件的触发规则）：
![image-20220807171511900](assets/image-20220807171511900.png)

注：配置完成后可通过发送测试邮件是否配置正确。



### Gitlab

gitlab是一个类似github/giree的源码托管平台，是一个开源项目，经常在企业中用于构建私有git仓库，托管企业内部的项目源代码，支持使用http以及ssh协议进行源码管理，支持使用svn/git源码管理工具。

官方地址：https://gitlab.com/



#### 使用docker-compose安装Gitlab

docker-compose.yaml，代码：

```yaml
version: '3.7'
services:
  gitlab:
    image: 'gitlab/gitlab-ce:latest' # gitlab的镜像，如果已经有了，指定自己的镜像版本即可
    container_name: gitlab # 生成的docker容器的名字
    restart: always
    environment:
      GITLAB_OMNIBUS_CONFIG: |
        external_url 'http://192.168.101.8:8993' # 此处填写所在服务器ip若有域名可以写域名
        gitlab_rails['gitlab_shell_ssh_port'] = 2224
    ports:
      - '8993:8993' # 此处端口号须与 external_url 中保持一致，左边和右边都要一样
      - '2224:22' # 这里的2224和上面的2224一致，但是右边必须是22，不能是其他
    volumes:
      #将相关配置映射到当前目录下的config目录
      - './conf/gitlab:/etc/gitlab'
      #将日志映射到当前目录下的logs目录
      - './logs/gitlab:/var/log/gitlab'
      #将数据映射到当前目录下的data目录
      - './data/gitlab:/var/opt/gitlab'

  jenkins:
    image: 'jenkins/jenkins:lts-jdk11'
    container_name: jenkins
    restart: always
    user: root
    environment:
      - TZ=Asia/Shanghai
    ports:
      - '8888:8080'
      - '5000:50000'
    volumes:
      - './data/jenkins:/var/jenkins_home'
```

终端下关闭原来的jenkins，并重启启动两个容器即可。

```bash
docker-compose down 
docker-compose up -d
```

gitlab容器启动以后，需要等待几分钟，接着在浏览器访问登陆地址：http://192.168.101.8:8993/

首次登陆需要创建一个管理员账号。





#### 基本使用

>注意：
>
>老师不知道各位同学的密码！！！自己设置的麻烦自己记一下哈。

刚安装完成的gitlab默认已经内置了一个超级管理员root，密码保存在文件配置目录下initial_root_password文件中。

![image-20220807174811289](assets/image-20220807174811289.png)

![image-20220807174923189](assets/image-20220807174923189.png)



直接使用上面的账号和密码登陆即可。

![image-20220807085758672](assets/image-20220807085758672.png)

登陆成功以后，配置中文界面。

![image-20220807175059923](assets/image-20220807175059923.png)

![image-20220807175140696](assets/image-20220807175140696.png)







## API调用

不管是jenkins还是gitlab实际上都提供了外界操作的http api接口给开发者进行远程调用的。

Gitlab RestAPI 文档：http://192.168.101.8:8993/help/api/api_resources.md

要使用Gitlab RestAPI需要配置访问令牌。

![image-20220807180743321](assets/image-20220807180743321.png)

![image-20220807180802431](assets/image-20220807180802431.png)

![image-20220807180817506](assets/image-20220807180817506.png)



有了令牌，就可以通过postman或者编程代码，使用http请求操作gitlab了。

![image-20220807181000029](assets/image-20220807181000029.png)



jenkins RestAPI：http://127.0.0.1:8888/api/

访问格式：http://账号:密码@服务端地址:端口/job/任务名/build

jenkins状态的API：http://127.0.0.1:8888/api/json?pretty=true



### Python调用Gitlab

操作文档：https://python-gitlab.readthedocs.io/en/master/api-usage.html

安装

```bash
pip install python-gitlab
```

#### 基本使用

连接gitlab

```python
import gitlab
url = "http://192.168.101.8"
token = "yussaW8kaV26qhbOL9A3pMrScD7D6HdHRU2vPufs"
gl = gitlab.Gitlab(url, token)
```

#### 常用操作

| 方法                                                         | 描述                                                         |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| projects =gl.projects.list(page=1)                           | 获取第一页project                                            |
| **`projects=gl.projects.list(all=True)`**                    | 获取所有的project                                            |
| **`projects=gl.projects.get(1)`**                            | 通过指定id 获取 project 对象                                 |
| **`projects = gl.projects.list(search='keyword')`**          | 查找项目                                                     |
| **`projects = gl.projects.list(visibility='public')`**       | 获取公开的项目，参数visibility的值：<br>public  公有项目<br>internal 内部项目<br>private 私有项目 |
| **`project = gl.projects.create({'name': 'test2', 'description': '测试项目2','visibility': 'public'})`** | 创建一个项目                                                 |
| **`branches = project.branches.list()`**                     | 通过指定project对象获取该项目的所有分支                      |
| **`branch = project.branches.get('main')`**                  | 获取指定分支的属性                                           |
| **`branch = project.branches.create({'branch_name': 'feature/user','ref': 'main'})`** | 创建分支                                                     |
| project.branches.delete('feature/user')                      | 删除分支                                                     |
| branch.protect()                                             | 分支保护[v4版本没有该功能]                                   |
| branch.unprotect()                                           | 取消保护[v4版本没有该功能]                                   |
| **`tags = project.tags.list()`**                             | 获取指定项目的所有tags                                       |
| **`tag = project.tags.get('v1.0')`**                         | 获取某个指定tag 的信息                                       |
| **`tag = project.tags.create({'tag_name':'v1.0', 'ref':'main'})`** | 创建一个tag                                                  |
| tag.set_release_description('v1.0 release')                  | 设置tags 说明                                                |
| project.tags.delete('v1.0')                                  | 删除tags                                                     |
| tag.delete()                                                 | 删除tags                                                     |
| **commits = project.commits.list()**                         | 获取所有commit                                               |
| data = {<br/>    'branch_name': 'master',  # v3<br/>    'commit_message': 'commit message description',<br/>    'actions': [<br/>        {<br/>            'action': 'create',<br/>            'file_path': '.',<br/>            'content': 'blah'<br/>        }<br/>    ]<br/>}<br/>**`commit = project.commits.create(data)`**<br/> | 创建一个commit                                               |
| **`commit = project.commits.get('d3a5171b')`**               | 获取指定commit                                               |
| mrs = project.mergerequests.list()                           | 获取指定项目的所有merge request                              |
| mr = project.mergerequests.get(mr_id)                        | 获取 指定merge request                                       |
| project.mergerequests.create({'source_branch':'cool_feature', 'target_branch':'master', 'title':'merge cool feature', }) | 创建一个merge request                                        |
| mr.description = 'merge description'                         | 更新一个merge request 的描述                                 |
| mr.state_event = 'close'  <br>mr.save()                      | 开关一个merge request  (close or reopen)                     |
| project.mergerequests.delete(mr_id)                          | 删除一个merge request                                        |
| mr.merge()                                                   | 通过一个merge request                                        |
| mrs = project.mergerequests.list(state='merged', sort='asc') | 指定条件过滤 所有的merge request<br>state：all、merged、opened、closed<br>sort：asc、desc |
| gl.users.list()                                              | 所有用户列表                                                 |

基本使用

```python
import gitlab

if __name__ == '__main__':
    """获取所有项目列表"""
    url = "http://192.168.101.8:8993/"
    token = "LAgbKLyaysE4UjPyX1EV"
    gl = gitlab.Gitlab(url, token)
    # print(gl)

    # """获取所有项目列表"""
    # projects = gl.projects.list(all=True)
    # for project in projects:
    #     print(project.id, project.name ,project.description)
    #
    #
    # """获取单个项目"""
    # project = gl.projects.get(2)
    #
    # print("项目ID", project.id)
    # print("项目描述", project.description)
    # print("项目名", project.name)
    # print("创建时间", project.created_at)
    # print("默认主分支", project.default_branch)
    # print("tag数量", len(project.tag_list))
    # print("仓库地址[ssh]", project.ssh_url_to_repo)
    # print("仓库地址[http]", project.http_url_to_repo)
    # print("仓库访问地址", project.web_url)
    # print("仓库可见性", project.visibility)  # internal 内部项目 public 开源项目   private私有项目
    # print("仓库派生数量", project.forks_count)
    # print("仓库星标数量", project.star_count)
    # print("仓库拥有者", getattr(project, "owner", None)) # 因为默认的第一个仓库是没有拥有者的!!
    #
    #
    #
    # """
    # {
    #     'id': 2,
    #     'description': '自动化运维平台',
    #     'name': 'uric',
    #     'name_with_namespace': 'Administrator / uric',
    #     'path': 'uric',
    #     'path_with_namespace': 'root/uric',
    #     'created_at': '2022-08-20T03:34:48.446Z',
    #     'default_branch': 'main',
    #     'tag_list': [],
    #     'topics': [],
    #     'ssh_url_to_repo': 'ssh://git@192.168.101.8:2224/root/uric.git',
    #     'http_url_to_repo': 'http://192.168.101.8:8993/root/uric.git',
    #     'web_url': 'http://192.168.101.8:8993/root/uric',
    #     'readme_url': 'http://192.168.101.8:8993/root/uric/-/blob/main/README.md',
    #     'avatar_url': None,
    #     'forks_count': 0,
    #     'star_count': 0,
    #     'last_activity_at': '2022-08-20T03:34:48.446Z',
    #     'namespace': {
    #         'id': 1,
    #         'name': 'Administrator',
    #         'path': 'root',
    #         'kind': 'user',
    #         'full_path': 'root',
    #         'parent_id': None,
    #         'avatar_url': 'https://www.gravatar.com/avatar/e64c7d89f26bd1972efa854d13d7dd61?s=80&d=identicon',
    #         'web_url': 'http://192.168.101.8:8993/root'
    #     },
    #     '_links': {
    #         'self': 'http://192.168.101.8:8993/api/v4/projects/2',
    #         'issues': 'http://192.168.101.8:8993/api/v4/projects/2/issues',
    #         'merge_requests': 'http://192.168.101.8:8993/api/v4/projects/2/merge_requests',
    #         'repo_branches': 'http://192.168.101.8:8993/api/v4/projects/2/repository/branches',
    #         'labels': 'http://192.168.101.8:8993/api/v4/projects/2/labels',
    #         'events': 'http://192.168.101.8:8993/api/v4/projects/2/events',
    #         'members': 'http://192.168.101.8:8993/api/v4/projects/2/members'
    #     },
    #     'packages_enabled': True,
    #     'empty_repo': False,
    #     'archived': False,
    #     'visibility': 'internal',
    #     'owner': {
    #         'id': 1,
    #         'username': 'root',
    #         'name': 'Administrator',
    #         'state': 'active',
    #         'avatar_url': 'https://www.gravatar.com/avatar/e64c7d89f26bd1972efa854d13d7dd61?s=80&d=identicon',
    #         'web_url': 'http://192.168.101.8:8993/root'},
    #         'resolve_outdated_diff_discussions': False,
    #         'container_expiration_policy': {'cadence': '1d',
    #         'enabled': False,
    #         'keep_n': 10,
    #         'older_than': '90d',
    #         'name_regex': '.*',
    #         'name_regex_keep': None,
    #         'next_run_at': '2022-08-21T03:34:49.221Z'},
    #         'issues_enabled': True,
    #         'merge_requests_enabled': True,
    #         'wiki_enabled': True,
    #         'jobs_enabled': True,
    #         'snippets_enabled': True,
    #         'container_registry_enabled': True,
    #         'service_desk_enabled': False,
    #         'service_desk_address': None,
    #         'can_create_merge_request_in': True,
    #         'issues_access_level': 'enabled',
    #         'repository_access_level': 'enabled',
    #         'merge_requests_access_level': 'enabled',
    #         'forking_access_level': 'enabled',
    #         'wiki_access_level': 'enabled',
    #         'builds_access_level': 'enabled',
    #         'snippets_access_level': 'enabled',
    #         'pages_access_level': 'private',
    #         'operations_access_level': 'enabled',
    #         'analytics_access_level': 'enabled',
    #         'container_registry_access_level': 'enabled',
    #         'emails_disabled': None,
    #         'shared_runners_enabled': True,
    #         'lfs_enabled': True,
    #         'creator_id': 1,
    #         'import_status': 'none',
    #         'open_issues_count': 0,
    #         'ci_default_git_depth': 50,
    #         'ci_forward_deployment_enabled': True,
    #         'ci_job_token_scope_enabled': False,
    #         'public_jobs': True,
    #         'build_timeout': 3600,
    #         'auto_cancel_pending_pipelines': 'enabled',
    #         'build_coverage_regex': None,
    #         'ci_config_path': None,
    #         'shared_with_groups': [],
    #         'only_allow_merge_if_pipeline_succeeds': False,
    #         'allow_merge_on_skipped_pipeline': None,
    #         'restrict_user_defined_variables': False,
    #         'request_access_enabled': True,
    #         'only_allow_merge_if_all_discussions_are_resolved': False,
    #         'remove_source_branch_after_merge': True,
    #         'printing_merge_request_link_enabled': True,
    #         'merge_method': 'merge',
    #         'squash_option': 'default_off',
    #         'suggestion_commit_message': None,
    #         'merge_commit_template': None,
    #         'squash_commit_template': None,
    #         'auto_devops_enabled': True,
    #         'auto_devops_deploy_strategy': 'continuous',
    #         'autoclose_referenced_issues': True,
    #         'repository_storage': 'default',
    #         'keep_latest_artifact': True,
    #         'permissions': {
    #             'project_access': {
    #                 'access_level': 40,
    #                 'notification_level': 3
    #             },
    #             'group_access': None
    #         }
    #     }
    # """

    # """根据项目名搜索项目"""
    # projects = gl.projects.list(search='uric')
    # print(projects)


    # """根据项目的可见性列出符合条件的项目"""
    # # projects = gl.projects.list(visibility='public')  # 公有项目列表
    # projects = gl.projects.list(visibility='private') # 私有项目列表
    # # projects = gl.projects.list(visibility='internal') # 内部项目列表
    # print(projects)

    """创建一个项目"""
    # project = gl.projects.create({
    #     'name': 'test2',   # 项目名，不要使用中文或其他特殊符号
    #     # 'path': 'test2',   # 访问路径，如果不设置path，则path的值默认为name
    #     'description': '测试项目2',
    #     'visibility': 'public'
    # })

    # """更新一个项目"""
    # # 先获取项目
    # project = gl.projects.get(5)
    # # 在获取了项目以后，直接对当前项目对象设置属性进行覆盖，后面调用save方法即可保存更新内容
    # project.description = "测试项目2的描述信息被修改了1次"
    # project.save()

    # """删除一个项目"""
    # project = gl.projects.get(5)
    # project.delete()



    # """分支管理：获取所有分支"""
    # project = gl.projects.get(3)
    # # branches = project.branches.list()
    # # print(branches)  # [<ProjectBranch name:main>]
    #
    # """根据名称获取一个分支"""
    # project = gl.projects.get(3)
    # branch = project.branches.get('main')
    # print("分支名称：", branch.name)
    # print("分支最新提交记录：", branch.commit)
    # print("分支合并状态：", branch.merged)
    # print("是否属于保护分支：", branch.protected)
    # print("当前分支是否可以推送代码：", branch.can_push)
    # print("是否是默认分支：", branch.default)
    # print("当前分支的访问路径：", branch.web_url)
    #
    # """
    # {
    #     'name': 'main',
    #     'commit': {
    #         'id': 'be71595d791b3437dee7e36a9dc221376392912f',
    #         'short_id': 'be71595d',
    #         'created_at': '2022-08-20T04:00:44.000+00:00',
    #         'parent_ids': [],
    #         'title': 'Initial commit',
    #         'message': 'Initial commit',
    #         'author_name': 'Administrator',
    #         'author_email': 'admin@example.com',
    #         'authored_date': '2022-08-20T04:00:44.000+00:00',
    #         'committer_name': 'Administrator',
    #         'committer_email': 'admin@example.com',
    #         'committed_date': '2022-08-20T04:00:44.000+00:00',
    #         'trailers': {},
    #         'web_url': 'http://192.168.101.8:8993/root/tools/-/commit/be71595d791b3437dee7e36a9dc221376392912f'
    #     },
    #     'merged': False,
    #     'protected': True,
    #     'developers_can_push': False,
    #     'developers_can_merge': False,
    #     'can_push': True,
    #     'default': True,
    #     'web_url': 'http://192.168.101.8:8993/root/tools/-/tree/main'
    # """

    # """给指定项目创建分支"""
    # project = gl.projects.get(3)
    # branch = project.branches.create({'branch': 'feature/user', 'ref': 'main'})
    # print(branch)

    """更新分支的属性【gitbal的v4版本中没有保护分支和取消保护分支的功能】"""
    # project = gl.projects.get(3)
    # branch = project.branches.get('feature/user')
    # # 设置当前分支为保护分支
    # branch.protect()


    # """删除一个分支"""
    # # 注意，只有一个保护分支时，是不能删除当前分支的
    # project = gl.projects.get(3)
    # project.branches.delete('feature/user')

    # """创建一个tag标签"""
    # project = gl.projects.get(3)
    # tag = project.tags.create({'tag_name': 'v1.0', 'ref': 'main'})
    # print(tag)

    # """获取所有tag标签"""
    # project = gl.projects.get(3)
    # tags = project.tags.list(all=True)
    # print(tags)

    # """获取一个tag标签信息"""
    # project = gl.projects.get(3)
    # tag = project.tags.get('v1.0')
    # print("标签名", tag.name)
    # print("标签的版本描述", tag.message)
    # print("标签的唯一标记(版本号)", tag.target) # 实际上就是本次创建标签时的分支最后一条commit的版本号
    # print("标签的最后一个commit记录", tag.commit)
    # print("当前标签是否发布", tag.release)
    # print("当前标签是佛属于保护标签", tag.protected)
    #
    # """
    # {
    #     'name': 'v1.0',
    #     'message': '',
    #     'target': 'be71595d791b3437dee7e36a9dc221376392912f',
    #     'commit': {
    #         'id': 'be71595d791b3437dee7e36a9dc221376392912f',
    #         'short_id': 'be71595d',
    #         'created_at': '2022-08-20T04:00:44.000+00:00',
    #         'parent_ids': [],
    #         'title': 'Initial commit',
    #         'message': 'Initial commit',
    #         'author_name': 'Administrator',
    #         'author_email': 'admin@example.com',
    #         'authored_date': '2022-08-20T04:00:44.000+00:00',
    #         'committer_name': 'Administrator',
    #         'committer_email': 'admin@example.com',
    #         'committed_date': '2022-08-20T04:00:44.000+00:00',
    #         'trailers': {},
    #         'web_url': 'http://192.168.101.8:8993/root/tools/-/commit/be71595d791b3437dee7e36a9dc221376392912f'
    #     },
    #     'release': None,
    #     'protected': False
    # }
    # """


    # """指定项目的commit提交记录"""
    # project = gl.projects.get(3)
    # commits = project.commits.list(all=True)
    # print(commits)

    # """根据版本号来获取commit记录"""
    # project = gl.projects.get(3)
    # commit = project.commits.get("be71595d791b3437dee7e36a9dc221376392912f")
    # print(commit)
    # """
    # {
    #     'id': 'be71595d791b3437dee7e36a9dc221376392912f',
    #     'short_id': 'be71595d',
    #     'created_at': '2022-08-20T04:00:44.000+00:00',
    #     'parent_ids': [],
    #     'title': 'Initial commit',
    #     'message': 'Initial commit',
    #     'author_name': 'Administrator',
    #     'author_email': 'admin@example.com',
    #     'authored_date': '2022-08-20T04:00:44.000+00:00',
    #     'committer_name': 'Administrator',
    #     'committer_email': 'admin@example.com',
    #     'committed_date': '2022-08-20T04:00:44.000+00:00',
    #     'trailers': {},
    #     'web_url': 'http://192.168.101.8:8993/root/tools/-/commit/be71595d791b3437dee7e36a9dc221376392912f',
    #     'stats': {
    #         'additions': 3,
    #         'deletions': 0,
    #         'total': 3},
    #         'status': None,
    #         'project_id': 3,
    #         'last_pipeline': None
    #     }
    # """


    # """创建一个commit版本"""
    # project = gl.projects.get(3)
    # data = {
    # 'branch': 'main',
    # 'commit_message': '提交代码的版本描述',
    #     'actions': [
    #         {
    #         'action': 'create',  # 创建文件
    #         # 'action': 'update',  # 更新文件
    #         # 'action': 'delete',    # 删除文件
    #         'file_path': 'docs/uric_api/logs/uric.log', # 文件路径
    #         'content': '上传文件的内容'  # 文件内容
    #         }
    #     ]
    # }
    #
    # commit = project.commits.create(data)


    """获取用户列表"""
    # print(gl.users.list())  # [<User id:1 username:root>]

    """获取单个用户信息"""
    user = gl.users.get(1)
    print(user)


```



封装工具类

```python
import gitlab


class Gitlabapi(object):
    VISIBILITY = {
        "private": "私有",
        "internal": "内部",
        "public": "公开"
    }

    def __init__(self, url, token):
        self.url = url
        self.token = token
        self.conn = gitlab.Gitlab(self.url, self.token)

    def get_projects(self):
        """
        获取所有的项目
        :return:
        """
        projects = self.conn.projects.list(all=True, iterator=True)
        projectslist = []
        for pro in projects:
            projectslist.append(pro.attributes)  # pro.attributes 项目的所有属性
        return projectslist

    def get_projects_visibility(self, visibility="public"):
        """
        根据可见性属性获取项目
        :param visibility:
        :return:
        """
        if visibility in self.VISIBILITY:
            attribute = visibility
        else:
            attribute = "public"
        projects = self.conn.projects.list(all=True, visibility=attribute)
        projectslist = []
        for pro in projects:
            projectslist.append(pro.attributes)
        return projectslist

    def get_projects_id(self, project_id):
        """
        根据id获取项目
        :param project_id:
        :return:
        """
        res = self.conn.projects.get(project_id)
        return res.attributes

    def get_projects_search(self, name):
        """
        模糊搜索项目
        :param name:
        :return:
        """
        projects = self.conn.projects.list(search=name)
        projectslist = []
        for pro in projects:
            projectslist.append(pro.attributes)
        return projectslist

    def create_project(self, name):
        """
        创建项目
        :param name:
        :return:
        """
        res = self.conn.projects.create({"name": name})
        return res.attributes

    def get_project_brances(self, project_id):
        """
        获取项目所有分支
        :param project_id:
        :return:
        """
        project = self.conn.projects.get(project_id)
        brancheslist = []
        for branches in project.branches.list():
            brancheslist.append(branches.attributes)
        return brancheslist

    def get_project_brance_attribute(self, project_id, branch):
        """
        获取指定项目指定分支
        :param project_id:
        :param branch:
        :return:
        """
        project = self.conn.projects.get(project_id)
        res = project.branches.get(branch)
        return res.attributes

    def create_get_project_brance(self, project_id, branch, ref="main"):
        """
        创建分支
        :param project_id:
        :param branch:
        :param ref:
        :return:
        """
        project = self.conn.projects.get(project_id)
        res = project.branches.create({"branch": branch, "ref": ref})
        return res.attributes

    def delete_project_brance(self, project_id, branch):
        """
        删除分支
        :param project_id:
        :param branch:
        :return:
        """
        project = self.conn.projects.get(project_id)
        project.branches.delete(branch)

    def protect_project_brance(self, project_id, branch, is_protect=None):
        """
        分支保护[v3.0可用, V4.0不可用]
        :param project_id:
        :param branch:
        :param is_protect:
        :return:
        """
        project = self.conn.projects.get(project_id)
        branch = project.branches.get(branch)
        if is_protect == "protect":
            branch.unprotect()
        else:
            branch.protect()

    def get_project_tags(self, project_id):
        """
        获取所有的tags标签
        :param project_id:
        :return:
        """
        project = self.conn.projects.get(project_id)
        tags = project.tags.list()
        taglist = []
        for tag in tags:
            taglist.append(tag.attributes)
        return taglist

    def get_project_tag_name(self, project_id, name):
        """
        获取指定的tag
        :param project_id:
        :param name:
        :return:
        """
        project = self.conn.projects.get(project_id)
        tags = project.tags.get(name)
        return tags.attributes

    def create_project_tag(self, project_id, name, branch="master"):
        """
        创建tag
        :param project_id:
        :param name:
        :param branch:
        :return:
        """
        project = self.conn.projects.get(project_id)
        tags = project.tags.create({"tag_name": name, "ref": branch})
        return tags.attributes

    def delete_project_tag(self, project_id, name):
        """
        删除tags
        :param project_id:
        :param name:
        :return:
        """
        project = self.conn.projects.get(project_id)
        project.tags.delete(name)

    def get_project_commits(self, project_id):
        """
        获取所有的commit
        :param project_id:
        :return:
        """
        project = self.conn.projects.get(project_id)
        commits = project.commits.list()
        commitslist = []
        for com in commits:
            commitslist.append(com.attributes)
        return commitslist

    def get_project_commit_info(self, project_id, commit_id):
        """
        获取指定的commit
        :param project_id:
        :param commit_id:
        :return:
        """
        project = self.conn.projects.get(project_id)
        commit = project.commits.get(commit_id)
        return commit.attributes

    def get_project_merge(self, project_id):
        """
        获取所有的合并请求
        :param project_id:
        :return:
        """
        project = self.conn.projects.get(project_id)
        mergerquests = project.mergerequests.list()
        mergerquestslist = []
        for mergerquest in mergerquests:
            mergerquestslist.append(mergerquest.attributes)
        return mergerquestslist

    def get_project_merge_id(self, project_id, mr_id):
        """
        获取请求的详细信息
        :param project_id:
        :param mr_id:
        :return:
        """
        project = self.conn.projects.get(project_id)
        mrinfo = project.mergerequests.get(mr_id)
        return mrinfo.attributes

    def create_project_merge(self, project_id, source_branch, target_branch, title):
        """
        创建合并请求
        :param project_id:
        :param source_branch:
        :param target_branch:
        :param title:
        :return:
        """
        project = self.conn.projects.get(project_id)
        res = project.mergerequests.create(
            {"source_branch": source_branch, "target_branch": target_branch, "title": title})
        return res

    def update_project_merge_info(self, project_id, mr_id, data):
        """
        更新合并请求的信息
        :param project_id:
        :param mr_id:
        :param data:
        :return:
        """
        # data = {"description":"new描述","state_event":"close"}
        project = self.conn.projects.get(project_id)
        mr = project.mergerequests.get(mr_id)
        if "description" in data:
            mr.description = data["description"]
        if "state_event" in data:
            state_event = ["close", "reopen"]
            if data["state_event"] in state_event:
                mr.state_event = data["state_event"]
        res = mr.save()
        return res

    def delete_project_merge(self, project_id, mr_id):
        """
        删除合并请求
        :param project_id:
        :param mr_id:
        :return:
        """
        project = self.conn.projects.get(project_id)
        res = project.mergerequests.delete(mr_id)
        return res

    def access_project_merge(self, project_id, mr_id):
        """
        允许合并请求
        :param project_id:
        :param mr_id:
        :return:
        """
        project = self.conn.projects.get(project_id)
        mr = project.mergerequests.get(mr_id)
        res = mr.merge()
        return res

    def search_project_merge(self, project_id, state, sort):
        '''
        搜索项目合并请求
        :param id:
        :param state: state of the mr,It can be one of all,merged,opened or closed
        :param sort: sort order (asc or desc)
        :param order_by: sort by created_at or updated_at
        :return:
        '''
        stateinfo = ["merged", "opened", "closed"]
        sortinfo = ["asc", "desc"]
        if state not in stateinfo:
            state = "merged"
        if sort not in sortinfo:
            sort = "asc"
        project = self.conn.projects.get(project_id)
        mergerquests = project.mergerequests.list(state=state, sort=sort)
        mergerquestslist = []
        for mergerquest in mergerquests:
            mergerquestslist.append(mergerquest.attributes)
        return mergerquestslist

    def create_project_commit(self, project_id, branch_name, message, actions):
        """
        创建项目提交记录
        :param project_id:
        :param branch_name:
        :param message:
        :param actions:
        :return:
        """
        project = self.conn.projects.get(project_id)
        data = {
            'branch': branch_name,
            'commit_message': message,
            'actions': actions,
            # 'actions': [{
            #     'action': 'create',
            #     'file_path': 'myreadme',
            #     'contend': 'commit_test'
            # }]
        }
        commit = project.commits.create(data)
        return commit

    def diff_project_branches(self, project_id, source_branch, target_branch):
        """
        比较2个分支
        :param project_id:
        :param source_branch:
        :param target_branch:
        :return:
        """
        project = self.conn.projects.get(project_id)
        result = project.repository_compare(source_branch, target_branch)
        # commits = result["commits"]
        # commits = result["diffs"]
        return result


if __name__ == '__main__':
    url = "http://192.168.101.8:8993/"
    token = "LAgbKLyaysE4UjPyX1EV"
    gl = Gitlabapi(url, token)
    # projects = gl.get_projects()
    projects = gl.get_projects_visibility("internal")
    print(projects)

```



### Python调用Jenkins

官方文档：https://python-jenkins.readthedocs.io/en/latest/

安装python-jenkins

```
pip install python-jenkins
```

#### 基本使用

基于密码/Token连接jenkins

```python
import jenkins
    # 基于登陆密码连接jenkins
    # server = jenkins.Jenkins('http://192.168.101.8:8888/', username='admin', password='7bb3d493057242edaf5a9e72c63ca27e')
    # 基于token连接jenkins
    server = jenkins.Jenkins('http://192.168.101.8:8888/', username='admin', password='11217915472cb72a7edb9a4de8113a5928')
    print(server)
```

#### token的获取方式

进入用户个人页面 —>  点击左上角的设置 —> API Token   —> 添加新 Token。 

![image-20220820155814261](assets/image-20220820155814261.png)



#### 常用操作

| 方法                                                         | 描述                                                         |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| `server.get_jobs()`                                          | 项目列表                                                     |
| `server.get_job_info('job名称')`                             | 根据名称获取执行项目                                         |
| `server.build_job(name='构建的job名称')`                     | 构建项目                                                     |
| `server.build_job(name='构建的job名称', parameters='构建的参数，字典类型')` | 参数化构建项目                                               |
| `server.stop_build('job名称', '构建编号ID')`                 | 停止一个正在运行的项目                                       |
| `server.enable_job('job名称')`                               | 激活项目状态为可构建                                         |
| `server.disable_job('job名称')`                              | 变更项目状态为不可构建                                       |
| `server.delete_job('job名称')`                               | 删除项目                                                     |
| `last_build_number = server.get_job_info('job名称')['lastBuild']['number']` | 获取项目当前构建的最后一次编号                               |
| `status = server.get_build_info('job名称', last_build_number)['result']` | 通过构建编号获取任务状态<br>状态有4种：SUCCESS、FAILURE、ABORTED、pending |
| `result = server.get_build_console_output(name='job名称', number=last_build_number)` | 获取项目控制台日志                                           |
| `result = server.get_build_test_report(name='job名称', number=last_build_number)` | 获取项目测试报告                                             |

快速入门，代码：

```python
import jenkins

if __name__ == '__main__':
    """连接jenkins"""
    # 基于登陆密码连接jenkins
    # server = jenkins.Jenkins('http://192.168.101.8:8888/', username='admin', password='7bb3d493057242edaf5a9e72c63ca27e')
    # 基于token连接jenkins
    server = jenkins.Jenkins('http://192.168.101.8:8888/', username='admin', password='11217915472cb72a7edb9a4de8113a5928')
    # print(server)

    # """我是谁?"""
    # user = server.get_whoami()
    # print(user)
    #
    # """jenkins的版本号"""
    # version = server.get_version()
    # print(version)

    # """查看所有的构建任务"""
    # jobs = server.get_jobs()
    # print(jobs)
    # """
    # [{
    #     '_class': 'hudson.model.FreeStyleProject',   # 构建项目的类型  FreeStyleProject 表示自由风格的构建项目
    #     'name': 'demo',                              # 构建项目的名称
    #     'url': 'http://192.168.101.8:8888/job/demo/',   # 访问地址
    #     'color': 'notbuilt',                            # 构建状态  【notbuilt, blue, 】
    #     'fullname': 'demo'                              # 构建项目的名称
    # }]
    # """

    # """获取指定的构建任务信息"""
    # info = server.get_job_info(name="demo")
    # print(info)
    # """
    # {
    #     '_class': 'hudson.model.FreeStyleProject',   # 构建项目类型
    #     'actions': [   # 构建项目的配置配置
    #         {},
    #         {},
    #         {'_class': 'org.jenkinsci.plugins.displayurlapi.actions.JobDisplayAction'},
    #         {'_class': 'com.cloudbees.plugins.credentials.ViewCredentialsAction'}
    #     ],
    #     'description': '测试构建项目',   # 构建项目的描述
    #     'displayName': 'demo',         # 构建项目的名称
    #     'displayNameOrNull': None,
    #     'fullDisplayName': 'demo',
    #     'fullName': 'demo',
    #     'name': 'demo',                # 构建项目的名称
    #     'url': 'http://192.168.101.8:8888/job/demo/',    # 访问地址
    #     'buildable': True,                               # 当前构建项目是否属于可构建状态（激活状态）
    #     'builds': [{                                     # 构建项目的执行记录
    #         '_class': 'hudson.model.FreeStyleBuild',
    #         'number': 1,
    #         'url': 'http://192.168.101.8:8888/job/demo/1/'
    #     }],
    #     'color': 'blue',                                 # 构建项目的执行状态（晴雨表）
    #     'firstBuild': {                                  # 首次构建的结果
    #         '_class': 'hudson.model.FreeStyleBuild',
    #         'number': 1,
    #         'url': 'http://192.168.101.8:8888/job/demo/1/'
    #     },
    #     'healthReport': [{                               # 构建项目的健康报告（晴雨表）
    #         'description': 'Build stability: No recent builds failed.',
    #         'iconClassName': 'icon-health-80plus',
    #         'iconUrl': 'health-80plus.png',
    #         'score': 100                                 # 构建任务的成功率
    #     }],
    #     'inQueue': False,                                # 是否处理队列等待中
    #     'keepDependencies': False,
    #     'lastBuild': {                                   # 上一次构建构建任务的状态
    #         '_class': 'hudson.model.FreeStyleBuild',
    #         'number': 1,
    #         'url': 'http://192.168.101.8:8888/job/demo/1/'},
    #         'lastCompletedBuild': {                     # 上一次完成构建的执行记录
    #             '_class': 'hudson.model.FreeStyleBuild',
    #             'number': 1,
    #             'url': 'http://192.168.101.8:8888/job/demo/1/'
    #         },
    #         'lastFailedBuild': None,                    # 上一次失败记录
    #         'lastStableBuild': {                        # 上次构建状态
    #             '_class': 'hudson.model.FreeStyleBuild',
    #             'number': 1,
    #             'url': 'http://192.168.101.8:8888/job/demo/1/'
    #         },
    #         'lastSuccessfulBuild': {                    # 上一次成功记录
    #             '_class': 'hudson.model.FreeStyleBuild',
    #             'number': 1,
    #             'url': 'http://192.168.101.8:8888/job/demo/1/'
    #         },
    #         'lastUnstableBuild': None,
    #         'lastUnsuccessfulBuild': None,
    #         'nextBuildNumber': 2,
    #         'property': [],
    #         'queueItem': None,
    #         'concurrentBuild': False,
    #         'disabled': False,
    #         'downstreamProjects': [],
    #         'labelExpression': None,
    #         'scm': {'_class': 'hudson.scm.NullSCM'},
    #         'upstreamProjects': []
    #     }
    # """

    # """开始构建任务"""
    # # 如果要构建的任务，不存在，则报错！！
    # build_id = server.build_job(name='demo')
    # print(build_id)

    # """设置构建任务为禁用状态(不可构建状态)"""
    # server.disable_job(name='demo')

    # """设置构建任务为激活激活状态(可构建状态)"""
    # server.enable_job(name="demo")

    # """删除一个构建任务"""
    # server.delete_job(name='demo')

    # """获取项目的最后一次构建编号"""
    # last_build_number = server.get_job_info('demo')['lastBuild']['number']
    # print(last_build_number)

    # """根据构建编号来获取构建结果"""
    # last_build_number = server.get_job_info('demo')['lastBuild']['number']
    # result = server.get_build_info('demo', last_build_number)['result']
    # print(result)  # SUCCESS

    # """根据构建编号获取构建过程中的终端输出内容"""
    # last_build_number = server.get_job_info('demo')['lastBuild']['number']
    # result = server.get_build_console_output(name='demo', number=last_build_number)
    # print(result)

    # """根据构建编号获取构建的测试报告【Allure】"""
    # last_build_number = server.get_job_info('demo')['lastBuild']['number']
    # result = server.get_build_test_report(name='demo', number=last_build_number)
    # print(result)

    """基于已有的任务，生成一份xml配置文档"""
    # config_xml = server.get_job_config(name="demo")
    # print(config_xml)

#     """
#     基于xml构建项目
#     """
#     config_xml = """<project>
# <description>测试构建项目</description>
# <keepDependencies>false</keepDependencies>
# <properties/>
# <scm class="hudson.scm.NullSCM"/>
# <canRoam>true</canRoam>
# <disabled>false</disabled>
# <blockBuildWhenDownstreamBuilding>false</blockBuildWhenDownstreamBuilding>
# <blockBuildWhenUpstreamBuilding>false</blockBuildWhenUpstreamBuilding>
# <triggers/>
# <concurrentBuild>false</concurrentBuild>
# <builders>
# <hudson.tasks.Shell>
#   <command>echo "hello, project-1"</command>
#   <configuredLocalRules/>
# </hudson.tasks.Shell>
# </builders>
# <publishers/>
# <buildWrappers/>
# </project>"""
#
#     server.create_job("project-1", config_xml=config_xml)

```

封装工具类，代码：

```python
import jenkins

class Jenkinsapi(object):
    def __init__(self,url, user, token):
        self.server_url = url
        self.user = user
        self.token = token
        self.conn = jenkins.Jenkins(self.server_url, username=self.user, password=self.token)

    def get_jobs(self):
        """
        获取所有的构建项目列表
        :return:
        """
        return self.conn.get_jobs()

    def get_job_info(self, job):
        """
        根据项目名获取构建项目
        :param job:
        :return:
        """
        return self.conn.get_job_info(job)

    def build_job(self,job,**kwargs):
        """
        开始构建项目
        :param job:
        :param kwargs:
        :return:
        """
        # dict1 = {"version":11} # 参数话构建
        # dict2 = {'Status': 'Rollback', 'BUILD_ID': '26'} # 回滚
        return self.conn.build_job(job, parameters=kwargs)

    def get_build_info(self,job, build_number):
        """
        通过构建编号获取构建项目的构建记录
        :param job:
        :param build_number:
        :return:
        """
        return self.conn.get_build_info(job,build_number)

    def get_job_config(self,job):
        '''
        获取xml文件
        '''
        res = self.conn.get_job_config(job)
        print(res)

    def create_job(self,name,config_xml):
        '''
        任务名字
        xml格式的字符串
        '''
        self.conn.create_job(name, config_xml)

    def update_job(self,name,config_xml):
        res = self.conn.reconfig_job(name,config_xml)
        print(res)


if __name__ == '__main__':
    server_url = 'http://192.168.101.8:8888/'
    username = 'admin'
    password = '11217915472cb72a7edb9a4de8113a5928'
    server = Jenkinsapi(server_url, username, password)

    # jobs = server.get_jobs()
    # print(jobs)

    # job = server.get_job_info("project-1")
    # print(job)

    # build_number = server.build_job("project-1")
    # print(build_number)

    # info = server.get_build_info("project-1", 2)
    # print(info)

    # 先获取已有构建项目的配置文档
    # config_xml = server.get_job_config("project-1")
    # print(config_xml)

    config_xml = """<project>
<description>测试构建项目</description>
<keepDependencies>false</keepDependencies>
<properties/>
<scm class="hudson.scm.NullSCM"/>
<canRoam>true</canRoam>
<disabled>false</disabled>
<blockBuildWhenDownstreamBuilding>false</blockBuildWhenDownstreamBuilding>
<blockBuildWhenUpstreamBuilding>false</blockBuildWhenUpstreamBuilding>
<triggers/>
<concurrentBuild>false</concurrentBuild>
<builders>
<hudson.tasks.Shell>
  <command>echo "hello, project-2"</command>
  <configuredLocalRules/>
</hudson.tasks.Shell>
</builders>
<publishers/>
<buildWrappers/>
</project>"""
    server.create_job("project-2", config_xml=config_xml)

```



## 环境管理

由于我们进行代码发布的时候，需要选择环境(测试环境、线上环境等等)，来区分我们本次将代码发布到什么环境的主机群组中。

所以我们先完成左侧菜单栏中环境管理。

![image-20210120142832689](assets/image-20210120142832689-1660964814922.png)



#### 后端实现环境管理的API接口

创建应用

```bash
cd uric_api/apps
python ../../manage.py startapp conf_center
```

配置应用，`settings/dev.py`，代码：

```python
INSTALLED_APPS = [
		...,
    'conf_center',
]
```

创建子应用路由文件，`conf_center/urls.py`，代码：

```python
from django.urls import path
from . import views

urlpatterns = [

]

```

总路由，`uric_api/urls`，代码：

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', include("home.urls")),
    path('host/', include("host.urls")),
    path('users/', include("users.urls")),
    path('mtask/', include('mtask.urls')),
    path('conf/', include('conf_center.urls')),
]
```

创建环境模型类，conf_center/models.py

```python
from uric_api.utils.models import BaseModel,models
# Create your models here.
class Environment(BaseModel):
    tag = models.CharField(max_length=32,verbose_name='标识符')
    class Meta:
        db_table = "uc_environment"
        verbose_name = "环境配置"
        verbose_name_plural = verbose_name
```

终端下在项目根目录下执行数据迁移。

```sql
python manage.py makemigrations
python manage.py migrate
```

在mysql中，执行SQL语句， 添加测试数据。

```sql
INSERT INTO uric.environment (id, name, is_show, orders, is_deleted, created_time, updated_time, description, tag) VALUES (1, '测试环境', 1, 1, 0, '2022-08-18 00:43:09', '2022-08-18 00:43:09', null, 'dev');
INSERT INTO uric.environment (id, name, is_show, orders, is_deleted, created_time, updated_time, description, tag) VALUES (2, '运营环境', 1, 1, 0, '2022-08-18 00:43:09', '2022-08-18 00:43:09', null, 'prod');
```

扩展host子应用的主机模型的字段，添加上主机和环境的关系。

host/models.py

```python
class Host(BaseModel):
    # 真正在数据库中的字段实际上叫 category_id，而category则代表了关联的哪个分类模型对象
    category = models.ForeignKey('HostCategory', on_delete=models.DO_NOTHING, verbose_name='主机类别', related_name='hc',
                                 null=True, blank=True)
    ip_addr = models.CharField(blank=True, null=True, max_length=500, verbose_name='连接地址')
    port = models.IntegerField(verbose_name='端口')
    username = models.CharField(max_length=50, verbose_name='登录用户')
    users = models.ManyToManyField(User)
    environment = models.ForeignKey(Environment, on_delete=models.DO_NOTHING, default=1, verbose_name='从属环境')

    class Meta:
        db_table = "host"
        verbose_name = "主机信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name + ':' + self.ip_addr

```

执行数据库数据迁移，同步数据结构：

```python
python manage.py makemigrations
python manage.py migrate
```

conf_center/urls，路由代码：

```python
from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register("env", views.EnvironmentAPIView, basename="env")

urlpatterns = [

] + router.urls

```

conf_center.views，视图代码：

```python
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Environment
from .serializers import EnvironmentModelSerializer
# Create your views here.


class EnvironmentAPIView(ModelViewSet):
    """
    环境管理的api接口
    """
    queryset = Environment.objects.all()
    serializer_class = EnvironmentModelSerializer
    permission_classes = [IsAuthenticated]

```

conf_center/serializers.py，序列化器代码：

```python
from rest_framework import serializers
from .models import Environment


class EnvironmentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Environment
        fields = ["id", "name", "tag", "description"]

```



#### 前端实现环境管理的功能

src/views/Environment.vue，代码：

```html
<template>
  <a-row>
    <a-col :span="20">
      <div class="add_host" style="margin: 15px;">
        <a-button @click="showEnvModal" type="primary">
          新建
        </a-button>
      </div>
    </a-col>
  </a-row>

  <a-table :dataSource="envList.data" :columns="envFormColumns">
    <template #bodyCell="{ column, text, record }">
      <template v-if="column.dataIndex === 'action'">
        <a-popconfirm
            v-if="envList.data.length"
            title="Sure to delete?"
            @confirm="deleteEnv(record)"
        >
          <a>Delete</a>
        </a-popconfirm>
        <a style="margin-left: 20px;" @click="showEnvUpdateModal(record)">Update</a>
      </template>
    </template>
  </a-table>

  <a-modal v-model:visible="envFormVisible" title="添加主机" @ok="onEnvFormSubmit" @cancel="resetForm()" :width="800">
    <a-form
        ref="formRef"
        name="custom-validation"
        :model="envForm.form"
        :rules="envForm.rules"
        v-bind="layout"
        @finish="handleFinish"
        @validate="handleValidate"
        @finishFailed="handleFinishFailed"
    >

      <a-form-item has-feedback label="环境名称" name="name">
        <a-input v-model:value="envForm.form.name" type="text" autocomplete="off"/>
      </a-form-item>

      <a-form-item has-feedback label="唯一标记符" name="tag">
        <a-input v-model:value="envForm.form.tag" type="text" autocomplete="off"/>
      </a-form-item>

      <a-form-item has-feedback label="备注信息" name="description">
        <a-textarea placeholder="请输入环境备注信息" v-model:value="envForm.form.description" type="text"
                    :auto-size="{ minRows: 3, maxRows: 5 }" autocomplete="off"/>
      </a-form-item>


      <a-form-item :wrapper-col="{ span: 14, offset: 4 }">
        <a-button @click="resetForm">Reset</a-button>
      </a-form-item>
    </a-form>


  </a-modal>
  <a-modal
      :width="600"
      title="新建主机类别"
      :visible="HostCategoryFromVisible"
      @cancel="hostCategoryFormCancel"
  >
    <template #footer>
      <a-button key="back" @click="hostCategoryFormCancel">取消</a-button>
      <a-button key="submit" type="primary" :loading="loading" @click="onHostCategoryFromSubmit">提交</a-button>
    </template>
    <a-form-model ref="hostCategoryRuleForm" v-model:value="hostCategoryForm.form" :rules="hostCategoryForm.rules"
                  :label-col="hostCategoryForm.labelCol" :wrapper-col="hostCategoryForm.wrapperCol">
      <a-form-model-item ref="name" label="类别名称" name="name">
        <a-row>
          <a-col :span="24">
            <a-input placeholder="请输入主机类别名称" v-model:value="hostCategoryForm.form.name"/>
          </a-col>
        </a-row>
      </a-form-model-item>
    </a-form-model>
  </a-modal>
  <!-- 批量导入主机 -->
  <div>
    <a-modal v-model:visible="excelVisible" title="导入excel批量创建主机" @ok="onExcelSubmit" @cancel="excelFormCancel"
             :width="800">
      <a-alert type="info" message="导入或输入的密码仅作首次验证使用，并不会存储密码。" banner closable/>
      <br/>

      <p>
        <a-form-item has-feedback label="模板下载" help="请下载使用该模板填充数据后导入">
          <a download="主机导入模板.xls">主机导入模板.xls</a>
        </a-form-item>
      </p>
      <p>
        <a-form-item label="默认密码"
                     help="如果Excel中密码为空则使用该密码">
          <a-input v-model:value="default_password" placeholder="请输入默认主机密码" type="password"/>
        </a-form-item>
      </p>
      <a-form-item label="导入数据">
        <div class="clearfix">
          <a-upload
              :file-list="fileList"
              name="file"
              :before-upload="beforeUpload"
          >
            <a-button>
              <upload-outlined></upload-outlined>
              Click to Upload
            </a-button>
          </a-upload>
        </div>
      </a-form-item>
    </a-modal>
    </div>

</template>
```

```vue
<script>
import {ref, reactive} from 'vue';
import axios from "axios";
import settings from "@/settings";
import store from "@/store";
import {message} from 'ant-design-vue';

export default {
  setup() {
    const formRef = ref();
    const HostCategoryFromVisible = ref(false);
    const envList = reactive({
      data: []
    })

    const envForm = reactive({
      labelCol: {span: 6},
      wrapperCol: {span: 14},
      other: '',
      form: {
        name: '',
        category: "",
        ip_addr: '',
        username: '',
        port: '',
        description: '',
        password: ''
      },
      rules: {
        name: [
          {required: true, message: '请输入环境名称', trigger: 'blur'},
          {min: 3, max: 30, message: '长度在3-10位之间', trigger: 'blur'}
        ],
        tag: [
          {required: true, message: '唯一标识符', trigger: 'blur'},
          {min: 3, max: 30, message: '长度在3-10位之间', trigger: 'blur'}
        ],
        description: [
          {required: true, message: '备注信息', trigger: 'blur'},
          {min: 1, max: 150, message: '长度在150位以内', trigger: 'blur'}
        ]
      }
    });

    const layout = {
      labelCol: {
        span: 4,
      },
      wrapperCol: {
        span: 14,
      },
    };

    const envFormColumns = [
        {
          title: 'ID',
          dataIndex: 'id',
          key: 'id',
          width: 100,
          sorter: {
            compare: (a, b) => a.id - b.id,
          },
        },
        {
          title: '环境名称',
          dataIndex: 'name',
          key: 'name',
          width: 200,
          sorter: {
            compare: (a, b) => a.name > b.name,
          },
        },
        {
          title: '唯一标记符',
          dataIndex: 'tag',
          key: 'tag',
          ellipsis: true,
          sorter: true,
          width: 200
        },
        {
          title: '备注',
          dataIndex: 'description',
          key: 'description',
          ellipsis: true
        },
        {
          title: '操作',
          key: 'action',
          width: 200,
          dataIndex: "action",
          scopedSlots: {customRender: 'action'}
        }
      ]

    const handleFinish = values => {
      console.log(values, envForm);
    };

    const handleFinishFailed = errors => {
      console.log(errors);
    };

    const resetForm = () => {
      formRef.value.resetFields();
    };

    const handleValidate = (...args) => {
      console.log(args);
    };

    const envFormVisible = ref(false);

    const showEnvModal = () => {
      envFormVisible.value = true;
    };


    // 提交添加环境的表单
    const onEnvFormSubmit = () => {
      // 将数据提交到后台进行保存，但是先进行连接校验，验证没有问题，再保存
      axios.post(`${settings.host}/conf/env/`, envForm.form, {
            headers: {
              Authorization: "jwt " + store.getters.token,
            }
          }
      ).then((response) => {
        console.log("response>>>", response)
        envList.data.unshift(response.data)
        // 清空
        resetForm()
        envFormVisible.value = false; // 关闭对话框
        message.success('成功添加主机信息！')

      }).catch((err) => {
        message.error('添加主机失败')
      });
    }

    const deleteEnv = record => {
      axios.delete(`${settings.host}/conf/env/${record.id}`, {
        headers: {
          Authorization: "jwt " + store.getters.token
        }
      }).then(response => {
        let index = envList.data.indexOf(record)
        envList.data.splice(index, 1);
      }).catch(err => {
        message.error('删除环境失败！')
      })
    }


    const get_env_list = () => {
      // 获取环境列表

      axios.get(`${settings.host}/conf/env`, {
        headers: {
          Authorization: "jwt " + store.getters.token
        }
      }).then(response => {
        envList.data = response.data
        console.log("envList.data=", envList.data)
      }).catch(err => {
        message.error('无法获取环境列表信息！')
      })
    }

    // 获取环境列表
    get_env_list()

    // 更新环境信息
    const showEnvUpdateModal = ()=>{

    }

    return {
      envForm,
      formRef,
      layout,
      HostCategoryFromVisible,
      handleFinishFailed,
      handleFinish,
      resetForm,
      handleValidate,
      envFormVisible,
      showEnvModal,
      onEnvFormSubmit,
      deleteEnv,
      envFormColumns,
      envList,
      showEnvUpdateModal,
    };
  },
};
</script>
```



路由，src/router/index.js，代码：

```javascript
import {createRouter, createWebHistory} from 'vue-router'
import ShowCenter from '../views/ShowCenter.vue'
import Login from '../views/Login.vue'
import Base from '../views/Base'
import Host from '../views/Host'
import Console from '../views/Console'
import MultiExec from '../views/MultiExec'
import Environment from '../views/Environment'
import store from "../store"

const routes = [
    {
        path: '/uric',
        alias: '/', // 给当前路径起一个别名
        name: 'Base',
        component: Base, // 快捷键：Alt+Enter快速导包
        children: [
            {
                meta: {
                    title: '展示中心',
                    authenticate: false,
                },
                path: 'show_center',
                alias: '',
                name: 'ShowCenter',
                component: ShowCenter
            },
            {
                meta: {
                    title: '资产管理',
                    authenticate: true,
                },
                path: 'host',
                name: 'Host',
                component: Host
            },
            {
                meta: {
                    title: 'Console',
                    authenticate: true,
                },
                path: 'console/:host_id',
                name: 'Console',
                component: Console
            },
            {
                path: 'multi_exec',
                name: 'MultiExec',
                component: MultiExec,
            },
            {
                path: 'environment',
                name: 'Environment',
                component: Environment,
            }
        ]
    },


    {
        meta: {
            title: '账户登陆',
            authenticate: false,
        },
        path: '/login',
        name: 'Login',
        component: Login // 快捷键：Alt+Enter快速导包
    },
];

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
})

router.beforeEach((to, from, next) => {
    document.title = to.meta.title;
    // console.log("to", to)
    // console.log("from", from)
    // console.log("store.getters.token:", store.getters.token)
    if (to.meta.authenticate && store.getters.token === "") {
        next({name: "Login"})
    } else {
        next()
    }
});

export default router


```



## 应用管理

所谓的应用，就是项目的代码（项目，更具体就是git仓库里面的提交代码版本）与数据（软件，mysql中的数据表）。



### 后端实现

创建代码发布功能的应用

```python
cd hippo_api/apps
python ../../manage.py startapp release
```

配置应用

```python
INSTALLED_APPS = [
		...,
    'release',
]
```

创建子医用release的路由文件，`release.urls`，代码：

```python
from django.urls import path
from . import views

urlpatterns = [
    # path('environment', views.EnvironmentAPIView.as_view()),
]
```

总路由，`hippo_api.urls`，代码：

```python
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("home.urls")),
    path("users/", include("users.urls")),
    path('host/', include('host.urls')),
    path('mtask/', include('mtask.urls')),
    path('conf_center/', include('conf_center.urls')),
    path('release/', include('release.urls')),
]
```

创建应用模型类

releaseApp/models.py

```python
from uric_api.utils.models import BaseModel,models
from users.models import User

# 发布应用表
class ReleaseApp(BaseModel):
    tag = models.CharField(max_length=32, unique=True, verbose_name='应用唯一标识号')
    user = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name='用户')
    class Meta:
        db_table = "hp_release_app"
        verbose_name = "应用管理"
        verbose_name_plural = verbose_name
```

数据迁移，项目根目录下，执行

```bash
python manage.py makemigrations
python manage.py migrate
```



release.urls，路由，代码：

```python
from django.urls import path
from . import views

urlpatterns = [
    path('app', views.ReleaseAPIView.as_view()),
]
```

release.views，视图，代码：

```python
from rest_framework.generics import ListAPIView,CreateAPIView
from .models import ReleaseApp
from .serializers import ReleaseAppModelSerializer
# Create your views here.
class ReleaseAPIView(ListAPIView,CreateAPIView):
    queryset = ReleaseApp.objects.all()
    serializer_class = ReleaseAppModelSerializer
```

release.serailizers，代码：

```python
from rest_framework import serializers
from .models import ReleaseApp
class ReleaseAppModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReleaseApp
        fields = ["id","name","tag","description"]
```

mysql执行SQL语句，添加测试数据。

```sql
INSERT INTO uric.uc_release_app (id, name, is_show, orders, is_deleted, created_time, updated_time, description, tag, user_id) VALUES (1, '购物车', 1, 1, 0, '2021-08-08 01:50:04', '2021-08-08 01:50:04', null, 'cart', 1);
INSERT INTO uric.uc_release_app (id, name, is_show, orders, is_deleted, created_time, updated_time, description, tag, user_id) VALUES (2, '支付模块', 1, 1, 0, '2021-08-08 01:50:04', '2021-08-08 01:50:04', null, 'pay', 1);
INSERT INTO uric.uc_release_app (id, name, is_show, orders, is_deleted, created_time, updated_time, description, tag, user_id) VALUES (3, '商品模块', 1, 1, 0, '2021-08-08 01:50:04', '2021-08-08 01:50:04', null, 'goods', 1);
```


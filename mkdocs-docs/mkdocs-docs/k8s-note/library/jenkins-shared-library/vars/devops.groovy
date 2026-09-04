import com.luffy.devops.*

/**
 *
 * @param repo, 10.211.55.27:5000/demo/myblog/xxx/
 * @param tag, v1.0
 * @param dockerfile
 * @param credentialsId
 * @param context
 */
def docker(String repo, String tag, String credentialsId, String dockerfile="Dockerfile", String context=".") {
    return new Docker().docker(repo, tag, credentialsId, dockerfile, context)
}
/**
 * 
 * @param resourcePath       # 源代码目录
 * @param watch              # Boolean watch表示让调用方可以选择同步 或者异步
 * @param workloadFilePath   # 这个目录是部署容器的 yaml文件目录
 * @return
 */
def deploy(String resourcePath, Boolean watch = true, String workloadFilePath){
    return new Deploy().init(resourcePath, watch, workloadFilePath)
}

/**
 * notificationSuccess
 * @param project
 * @param receiver
 * @param credentialsId
 * @param title
 * @return
 */
def notificationSuccess(String project, String receiver="dingTalk", String credentialsId="dingTalk", String title=""){
    new Notification().getObject(project, receiver, credentialsId, title).notification("success")
}

/**
 * notificationFailed
 * @param project
 * @param receiver
 * @param credentialsId
 * @param title
 * @return
 */
def notificationFailed(String project, String receiver="dingTalk", String credentialsId="dingTalk", String title=""){
    new Notification().getObject(project, receiver, credentialsId, title).notification("failure")
}

/**
 * sonarqube scanner
 * @param projectVersion
 * @param waitScan
 * @return
 */
def scan(String projectVersion="", Boolean waitScan = true) {
    return new Sonar().init(projectVersion, waitScan)
}

/**
 * 
 * @param comp
 * @return
 */
def robotTest(String comp=""){
    new Robot().acceptanceTest(comp)
}

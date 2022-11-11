package com.luffy.devops

import org.yaml.snakeyaml.Yaml
import groovy.json.JsonSlurperClassic
import groovy.time.TimeCategory

def init(String resourcePath, Boolean watch, String workloadFilePath) {
    this.resourcePath = resourcePath
    this.msg = new BuildMessage()
    this.watch = watch
    this.workloadFilePath = workloadFilePath
    if(!resourcePath && !workloadFilePath){
        throw Exception("illegal resource path")
    }
    return this
}

def start(){
    try{
        // sh "sed -i 's#{{IMAGE_URL}}#${env.CURRENT_IMAGE}#g' ${this.resourcePath}/*"
	this.tplHandler()
        sh "kubectl apply -f ${this.resourcePath}"
    } catch (Exception exc){
        updateGitlabCommitStatus(name: env.STAGE_NAME, state: 'failed')
        this.msg.updateBuildMessage(env.BUILD_TASKS, "${env.stage_name} fail...  √")
        throw exc
    }

    if (this.watch) {
        // 初始化workload文件
        initWorkload()
        String namespace = this.workloadNamespace
        String name = env.workloadName
        if(env.workloadType.toLowerCase() == "deployment"){
            echo "begin watch pod status from deployment ${env.workloadName}..."
            monitorDeployment(namespace, name)
        }else {
            //todo
            echo "workload type ${env.workloadType} does not support for now..."
        }

    }else {
        updateGitlabCommitStatus(name: env.STAGE_NAME, state: 'success')
        this.msg.updateBuildMessage(env.BUILD_TASKS, "${env.STAGE_NAME} OK...  √")
    }
}

def tplHandler(){
    sh "sed -i 's#{{IMAGE_URL}}#${env.CURRENT_IMAGE}#g' ${this.resourcePath}/*"
    String namespace = "dev"
    if(env.TAG_NAME){
        namespace = "test"
    }
    try {
        def configMapData = this.getResource(namespace, "devops-config", "configmap")["data"]
        configMapData.each { k, v ->
            echo "key is ${k}, val is ${v}"
            sh "sed -i 's#{{${k}}}#${v}#g' ${this.resourcePath}/*"
        }
    }catch (Exception exc) {
        echo "failed to get devops-config data,exception: ${exc}."
        throw exc
    }
}
def initWorkload() {
    try {
        def content = readFile this.workloadFilePath
        Yaml parser = new Yaml()
        def data = parser.load(content)
        def kind = data["kind"]
        if (!kind) {
            throw Exception("workload file ${kind} illegal, will exit pipeline!")
        }
        env.workloadType = kind
        echo "${data}"
        this.workloadNamespace = data["metadata"]["namespace"]
        if (!this.workloadNamespace){
            this.workloadNamespace = "default"
        }
        env.workloadName = data["metadata"]["name"]

    } catch (Exception exc) {
        echo "failed to readFile ${this.workloadFilePath},exception: ${exc}."
        throw exc
    }
}

/**
 *
 * @param namespace
 * @param name
 * @param timeoutMinutes
 * @param sleepTime
 * @return
 */
def monitorDeployment(String namespace, String name, int timeoutMinutes = 5, sleepTime = 3) {
    def readyCount = 0
    def readyTarget = 3
    use( TimeCategory ) {
        def endTime = TimeCategory.plus(new Date(), TimeCategory.getMinutes(timeoutMinutes))
        def lastRolling
        while (true) {
            // checking timeout
            if (new Date() >= endTime) {
                echo "timeout, printing logs..."
                this.printContainerLogs(lastRolling)
                updateGitlabCommitStatus(name: 'deploy', state: 'failed')
                this.msg.updateBuildMessage(env.BUILD_TASKS, "${env.STAGE_NAME} Failed...  x")
                throw new Exception("deployment timed out...")
            }
            // checking deployment status
            try {
                def rolling = this.getResource(namespace, name, "deployment")
                lastRolling = rolling
                if (this.isDeploymentReady(rolling)) {
                    readyCount++
                    echo "ready total count: ${readyCount}"
                    if (readyCount >= readyTarget) {
                        updateGitlabCommitStatus(name: env.STAGE_NAME, state: 'success')
                        this.msg.updateBuildMessage(env.BUILD_TASKS, "${env.STAGE_NAME} OK...  √")
                        break
                    }

                } else {
                    readyCount = 0
                    echo "reseting ready total count: ${readyCount}，print pods event logs"
                    this.printContainerLogs(lastRolling)
                    sh "kubectl get pod -n ${namespace} -o wide"
                }
            } catch (Exception exc) {
                updateGitlabCommitStatus(name: 'deploy', state: 'failed')
                this.msg.updateBuildMessage(env.BUILD_RESULT, "${env.STAGE_NAME} Failed...  ×")
                echo "error: ${exc}"
            }
            sleep(sleepTime)
        }
    }
    return this
}

def getResource(String namespace = "default", String name, String kind="deployment") {
    sh "kubectl get ${kind} -n ${namespace} ${name} -o json > ${namespace}-${name}-yaml.yml"
    def jsonStr = readFile "${namespace}-${name}-yaml.yml"
    def jsonSlurper = new JsonSlurperClassic()
    def jsonObj = jsonSlurper.parseText(jsonStr)
    return jsonObj
}

def printContainerLogs(deployJson) {
    if (deployJson == null) {
        return;
    }
    def namespace = deployJson.metadata.namespace
    def name = deployJson.metadata.name
    def labels=""
    deployJson.spec.template.metadata.labels.each { k, v ->
        labels = "${labels} -l=${k}=${v}"
    }
    sh "kubectl describe pods -n ${namespace} ${labels}"
}

def isDeploymentReady(deployJson) {
    def status = deployJson.status
    def replicas = status.replicas
    def unavailable = status['unavailableReplicas']
    def ready = status['readyReplicas']
    if (unavailable != null) {
        return false
    }
    def deployReady = (ready != null && ready == replicas)
    // get pod information
    if (deployJson.spec.template.metadata != null && deployReady) {
        if (deployJson.spec.template.metadata.labels != null) {
            def labels=""
            def namespace = deployJson.metadata.namespace
            def name = deployJson.metadata.name
            deployJson.spec.template.metadata.labels.each { k, v ->
                labels = "${labels} -l=${k}=${v}"
            }
            if (labels != "") {
                sh "kubectl get pods -n ${namespace} ${labels} -o json > ${namespace}-${name}-json.json"
                def jsonStr = readFile "${namespace}-${name}-json.json"
                def jsonSlurper = new JsonSlurperClassic()
                def jsonObj = jsonSlurper.parseText(jsonStr)
                def totalCount = 0
                def readyCount = 0
                jsonObj.items.each { k, v ->
                    echo "pod phase ${k.status.phase}"
                    if (k.status.phase != "Terminating" && k.status.phase != "Evicted") {
                        totalCount++;
                        if (k.status.phase == "Running") {
                            readyCount++;
                        }
                    }
                }
                echo "Pod running count ${totalCount} == ${readyCount}"
                return totalCount > 0 && totalCount == readyCount && totalCount == replicas
            }
        }
    }
    return deployReady
}


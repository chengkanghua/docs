package com.luffy.devops


def init(String projectVersion="", Boolean waitScan = true) {
    this.waitScan = waitScan
    this.msg = new BuildMessage()
    if (projectVersion == ""){
	sh "git config --global --add safe.directory /home/jenkins/agent/workspace/multi-branch-myblog_master"
        projectVersion = sh(returnStdout: true, script: 'git log --oneline -n 1|cut -d " " -f 1')
    }
    sh "echo '\nsonar.projectVersion=${projectVersion}' >> sonar-project.properties"
    sh "cat sonar-project.properties"
    return this
}

def start() {
    try {
        this.startToSonar()
    }
    catch (Exception exc) {
        throw exc
    }
    return this
}

def startToSonar() {
    withSonarQubeEnv('sonarqube') {
        sh "sonar-scanner -X;"
        sleep 5
    }
    if(this.waitScan){
        //wait 3min
        timeout(time: 3, unit: 'MINUTES') {
            def qg = waitForQualityGate()
            String stage = "${env.stage_name}"
            if (qg.status != 'OK') {
                this.msg.updateBuildMessage(env.BUILD_TASKS, "${stage} Failed...  ×")
                updateGitlabCommitStatus(name: "${stage}", state: 'failed')
                error "Pipeline aborted due to quality gate failure: ${qg.status}"
            }else{
                this.msg.updateBuildMessage(env.BUILD_RESULT, "${stage} OK...  √")
                updateGitlabCommitStatus(name: "${stage}", state: 'success')
            }
        }
    }else{
        echo "skip waitScan"
    }
    return this
}

package com.luffy.devops

/**
 *
 * @param repo
 * @param tag
 * @param credentialsId
 * @param dockerfile
 * @param context
 * @return
 */
def docker(String repo, String tag, String credentialsId, String dockerfile="Dockerfile", String context="."){
    this.repo = repo
    this.tag = tag
    if(env.TAG_NAME){
        this.tag = env.TAG_NAME
    }
    this.dockerfile = dockerfile
    this.credentialsId = credentialsId
    this.context = context
    this.fullAddress = "${this.repo}:${this.tag}"
    this.isLoggedIn = false
    this.msg = new BuildMessage()
    return this
}


/**
 * build image
 * @return
 */
def build() {
    this.login()
    def isSuccess = false
    def errMsg = ""
    retry(3) {
        try {
            sh "docker build ${this.context} -t ${this.fullAddress} -f ${this.dockerfile} "
            isSuccess = true
        }catch (Exception err) {
            //ignore
            errMsg = err.toString()
        }
        // check if build success
        def stage = env.STAGE_NAME + '-build'
        if(isSuccess){
            updateGitlabCommitStatus(name: "${stage}", state: 'success')
            this.msg.updateBuildMessage(env.BUILD_TASKS, "${stage} OK...  √")
        }else {
            updateGitlabCommitStatus(name: "${stage}", state: 'failed')
            this.msg.updateBuildMessage(env.BUILD_TASKS, "${stage} Failed...  x")
            // throw exception，aborted pipeline
            error errMsg
        }

        return this
    }
}


/**
 * push image
 * @return
 */
def push() {
    this.login()
    def isSuccess = false
    def errMsg = ""
    retry(3) {
        try {
            sh "docker push ${this.fullAddress}"
	    env.CURRENT_IMAGE = this.fullAddress
            isSuccess = true
        }catch (Exception err) {
            //ignore
            errMsg = err.toString()
        }
    }
    // check if build success
    def stage = env.STAGE_NAME + '-push'
    if(isSuccess){
        updateGitlabCommitStatus(name: "${stage}", state: 'success')
        this.msg.updateBuildMessage(env.BUILD_TASKS, "${stage} OK...  √")
    }else {
        updateGitlabCommitStatus(name: "${stage}", state: 'failed')
        this.msg.updateBuildMessage(env.BUILD_TASKS, "${stage} Failed...  x")
        // throw exception，aborted pipeline
        error errMsg
    }
    return this
}

/**
 * docker registry login
 * @return
 */
def login() {
    if(this.isLoggedIn || credentialsId == ""){
        return this
    }
    // docker login
    withCredentials([usernamePassword(credentialsId: this.credentialsId, usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {
        def regs = this.getRegistry()
        retry(3) {
            try {
                sh "docker login ${regs} -u $USERNAME -p $PASSWORD"
            } catch (Exception ignored) {
                echo "docker login err, ${ignored.toString()}"
            }
        }
    }
    this.isLoggedIn = true;
    return this;
}

/**
 * get registry server
 * @return
 */
def getRegistry(){
    def sp = this.repo.split("/")
    if (sp.size() > 1) {
        return sp[0]
    }
    return this.repo
}

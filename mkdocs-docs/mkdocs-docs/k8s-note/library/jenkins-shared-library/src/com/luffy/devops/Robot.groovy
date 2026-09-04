package com.luffy.devops

def acceptanceTest(comp) {
    try{
        echo "Trigger to execute Acceptance Testing"
        def rf = build job: 'robot-cases',
                parameters: [
                        string(name: 'comp', value: comp)
                ],
                wait: true,
                propagate: false
        def result = rf.getResult()
        def msg = "${env.STAGE_NAME}... "
        if (result == "SUCCESS"){
            msg += "√ success"
        }else if(result == "UNSTABLE"){
            msg += "⚠ unstable"
        }else{
            msg += "× failure"
        }
        echo rf.getAbsoluteUrl()
        env.ROBOT_TEST_URL = rf.getAbsoluteUrl()
        new BuildMessage().updateBuildMessage(env.BUILD_TASKS, msg)
    } catch (Exception exc) {
        echo "trigger  execute Acceptance Testing exception: ${exc}"
        new BuildMessage().updateBuildMessage(env.BUILD_RESULT, msg)
    }
}

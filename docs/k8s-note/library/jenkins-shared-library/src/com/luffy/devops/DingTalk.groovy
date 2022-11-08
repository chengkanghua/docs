package com.luffy.devops

import groovy.json.JsonOutput


def sendRequest(method, data, credentialsId, Boolean verbose=false, codes="100:399") {
    def reqBody = new JsonOutput().toJson(data)
    withCredentials([usernamePassword(credentialsId: credentialsId, usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {
        def response = httpRequest(
                httpMode:method,
                url: "https://oapi.dingtalk.com/robot/send?access_token=${PASSWORD}",
                requestBody:reqBody,
                validResponseCodes: codes,
                contentType: "APPLICATION_JSON",
                quiet: !verbose
        )
    }
}

def markDown(String title, String text, String credentialsId, Boolean verbose=false) {
    def data = [
            "msgtype": "markdown",
            "markdown": [
                    "title": title,
                    "text": text
            ]
    ]
    this.sendRequest("POST", data, credentialsId, verbose)
}

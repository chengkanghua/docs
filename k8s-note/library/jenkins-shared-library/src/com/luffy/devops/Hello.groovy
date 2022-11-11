package com.luffy.devops

/**
 * @author Yongxin
 * @version v0.1
 */

/**
 * say hello
 * @param content
 */
def init(String content) {
    this.content = content
    return this
}


def sayHi() {
    echo "Hi, ${this.content},how are you?"
    return this
}

def answer() {
    echo "${this.content}: fine, thank you, and you?"
    return this
}

def sayBye() {
    echo "i am fine too , ${this.content}, Bye!"
    return this
}
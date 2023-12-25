<template>
  <div class="console">
    <div id="terminal"></div>
  </div>
</template>

<script>
import {Terminal} from 'xterm'
import settings from "../settings"

export default {
  name: "Console",
  mounted() {
    this.show_terminal()
  },
  methods: {
    show_terminal() {
      // 初始化terminal窗口
      let term = new Terminal({
        rendererType: "canvas", //渲染类型
        // rows: 40, //行数
        convertEol: true, // 启用时，光标将设置为下一行的开头
        scrollback: 100,   // 终端中的回滚量
        disableStdin: false, //是否应禁用输入。
        cursorStyle: 'underline', //光标样式
        cursorBlink: true, //光标闪烁
        theme: {
          foreground: '#ffffff', //字体
          background: '#060101', //背景色
          cursor: 'help',//设置光标
        }
      });

      // 建立websocket
      let ws = new WebSocket(`ws://api.uric.cn:8000/ws/ssh/${this.$route.params.host_id}/`);
      let cmd = '';  // 拼接用户输入的命令

      // 监听接收来自服务端响应的数据
      ws.onmessage = function (event) {
        if (!cmd) {
          //所要执行的操作
          term.write(event.data);
        } else {
          console.log(JSON.stringify(event.data))
          cmd = ''
          let res = event.data.replace(event.data.split('\r\n', 1)[0] + "\r\n", '');
          term.write('\r\n' + res)
        }
      }

      term.prompt = () => {
        term.write('\r\n');
        // term.write('\r\n$ ')
      }

      term.onKey(e => {
        console.log(e.key)
        const ev = e.domEvent
        const printable = !ev.altKey && !ev.altGraphKey && !ev.ctrlKey && !ev.metaKey

        if (ev.key === "Enter") {
          // 按下回车键进行指令的发送
          ws.send(cmd);

        } else if (ev.key === "BackSpace") {
          // Do not delete the prompt
          if (term._core.buffer.x > 2) {
            term.write('\b \b')
          }
        } else if (printable) {
          term.write(e.key);
          cmd += e.key
        }
      })

      term.open(document.getElementById('terminal'));

    }
  }
}
</script>

<style scoped>

</style>
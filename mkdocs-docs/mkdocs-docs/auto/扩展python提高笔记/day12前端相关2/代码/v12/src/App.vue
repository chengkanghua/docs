<template>
  <div id="app">
    <div>
      <router-link to="/index">首页</router-link>
      <router-link to="/course">课程</router-link>
      <router-link to="/news">科技</router-link>
    </div>

    <router-view/>

    <div class="pg-footer">
      <router-link class="item" to="/about">关于我们</router-link>
      <router-link class="item" to="/feedback">意见反馈</router-link>
      <router-link class="item" to="/user">新手指南 {{ctime}}</router-link>
    </div>
  </div>
</template>

<script>
  export default {
    name: 'App',
    data: function () {
      return {
        ctime: new Date()
      }
    }
  }
</script>

<style>
  .pg-footer .item{
    display: inline-block;
    padding: 10px;
    border: 1px solid red;
  }
</style>

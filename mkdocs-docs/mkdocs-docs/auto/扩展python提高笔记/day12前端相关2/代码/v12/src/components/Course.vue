<template>
  <div>
    <h1>课程列表</h1>

    <div>
      <input type="text" placeholder="ID" v-model="id">
      <input type="text" placeholder="姓名" v-model="name">
      <input type="text" placeholder="年龄" v-model="age">
      <input type="button" value="添加" v-on:click="doAdd">
    </div>
    <table border="1">
      <thead>
      <tr>
        <th>ID</th>
        <th>姓名</th>
        <th>年龄</th>
        <th>删除</th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="(item,index) in userList">
        <td>{{item.id}}</td>
        <td>{{item.name}}</td>
        <td>{{item.age}}</td>
        <td>
          <span v-on:click="doDelete(index)">删除</span>
        </td>
      </tr>
      </tbody>
    </table>

    <hr/>

    <div>从django获取数据</div>
    <ul v-for="item in djangoDataList">
      <li>{{item}}</li>
    </ul>
  </div>

</template>

<script>
  export default {
    name: "Course",
    data() {
      return {
        userList: [
          {id: 1, name: "alex", age: 73},
          {id: 2, name: "李杰", age: 84},
        ],
        id: "",
        name: "",
        age: "",
        djangoDataList: []
      }
    },
    mounted() {
      // this是vue对象

      // 当每次进入此页面时，该方法都会被触发。
      // 向django发送请求， 请求如果获取到数据
      this.$axios.request({
        url: "http://127.0.0.1:8000/api/",
        method: "get"
      }).then((res) => {
        // 发送成功并获取到结果后，自动执行此函数
        // 成功之后，res.data  赋值给 this.djangoDataList
        // console.log("获取成功", res);
        this.djangoDataList = res.data.values;
      }).catch(function (res) {
        // 发送失败时，自动执行此函数
      })

      // this.djangoDataList = [123, 123, 123]
    },
    methods: {
      doAdd() {

        // 找到input框中输入的内容，直接去读js中的id/name/age
        // 添加到table表格中，其实直接放在 userList 中。
        let row = {id: this.id, name: this.name, age: this.age};
        this.userList.push(row);
      },
      doDelete(index) {


        // 根据索引位置将userList中的数据删除
        this.userList.splice(index, 1);
      }
    }
  }
</script>

<style scoped>

</style>

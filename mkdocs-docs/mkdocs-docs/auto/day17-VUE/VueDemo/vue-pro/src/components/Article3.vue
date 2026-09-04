<template>
    <Nav/>
    <h1>{{year}}年 {{month}}月文章</h1>

    <ul>
        <li v-for="article in article_list">{{article}}</li>
    </ul>

</template>

<script>
    import Nav from '@/components/Nav.vue'

    export default {
        name: "Article",
        data() {
            return {
                year: "某年",
                month: "某月",
                article_list: ["西游记", "三国演义", "金瓶梅", "水浒传"],
            }
        },
        components: {
            Nav,
        },
        created() {
            var year = this.$route.query.year;
            var month = this.$route.query.month;
            // console.log("year", year);
            // console.log("month", month);
            this.year = year;
            this.month = month;
            // 发送ajax请求
            /*
            axios.get("",{
                params:{
                    year:year,
                    month:month
                }
            })
            */
        }
    }
</script>

<style scoped>
    ul {
        list-style: none;
        padding: 0;
    }

</style>
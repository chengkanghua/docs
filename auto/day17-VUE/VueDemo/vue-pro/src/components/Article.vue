<template>
    <Nav/>
    <h1>所有文章</h1>

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
        }
    }
</script>

<style scoped>
    ul {
        list-style: none;
        padding: 0;
    }

</style>
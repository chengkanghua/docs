<template>
    <div class="home">
        <!--    <img alt="Vue logo" src="../assets/logo.png">-->
        <!--    <HelloWorld msg="Welcome to Your Vue.js App"/>-->
        <Nav @getCity="callBack"></Nav>
        <p>选中的城市：{{city}}</p>
        <Forecast :choose_city="city"/>


    </div>
</template>

<script>
    // @ is an alias to /src
    import Nav from '@/components/Nav.vue'
    import Forecast from '@/components/Forecast.vue'
    import Article from '@/components/Article.vue'


    export default {
        name: 'Home',
        data() {
            return {
                city: ""
            }
        },
        components: {
            Nav,
            Forecast,
            Article

        },
        methods: {
            callBack(choose_city) {

                this.city = choose_city
            },
        }
    }
</script>

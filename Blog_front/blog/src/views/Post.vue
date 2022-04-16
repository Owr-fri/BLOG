<template>
    <div class="home">
        <Header/>
        <router-view></router-view>
        <Footer/>
    </div>
</template>

<script>
import Header from '@/components/Header.vue'
import Footer from '@/components/Footer.vue'

export default {
    name:"post",
    components:{
        Header,
        Footer,
    },
}
</script>

<style lang="less" scoped>
    .home{
        margin: 0px auto;
        width: 820px;
        min-height: 100%;
    }
    .footer{
        margin: 0px auto;
        width: 820px;
        height:45px;
        bottom:0px;
    }
</style>
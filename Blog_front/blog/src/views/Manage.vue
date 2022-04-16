<template>
    <div class="home">
        <Header/>
        <div class="main">
            <div class="nav-bar">
                <NavBar/>
            </div>
            <div class="activate-content">
                <el-empty :description="description" v-if="this.$route.path == '/manage'"></el-empty>
                <router-view></router-view>
            </div>
            <div class="clear"></div>
        </div>
        
        <Footer/>
    </div>
</template>

<script>
import Header from "@/components/Header.vue"
import Footer from '@/components/Footer.vue'
import NavBar from '@/components/NavBar.vue'

export default {
    name:'editor',
    components:{
        Header,
        Footer,
        NavBar,
    },
    data(){
        return {
            description:'请选择导航'
        }
    },

    mounted(){
    }
}
</script>

<style scoped>
    .home{
        margin: 0px auto;
        height: 100%;
        width: 900px;
    }
    .footer{
        margin: 0px auto;
        width: 940px;
        height:45px;
        bottom:0px;
    }
    .main{
        margin-top: 15px;
        min-height: calc(90vh);
    }
    .nav-bar{
        width: 155px;
        float: left;
    }
    .nav-bar >>> .el-col-4 {
        width: 100%!important;
    }
    .activate-content{
        width: 82%;
        float:right;
    }
    .clear{
        clear: both;
    }
</style>
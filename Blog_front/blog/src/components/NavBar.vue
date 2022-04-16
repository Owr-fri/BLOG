<template>
    <el-row class="tac">
        <el-col :span="4">
            <el-menu
            :default-active="this.$route.path"
            class="menu-bar"
            active-text-color="#3fc9be"
            text-color="#505560"
            :router="true">
                <el-submenu index="posts-manage">
                    <template slot="title">
                    <span>博客管理</span>
                    </template>
                    <el-menu-item-group>
                    <el-menu-item index="/manage/publishpost">发表博客</el-menu-item>
                    <el-menu-item index="/manage/postm">管理博客</el-menu-item>
                    </el-menu-item-group>
                </el-submenu>
                <el-submenu index="picture-manage">
                    <template slot="title">
                    <span>图集管理</span>
                    </template>
                    <el-menu-item-group>
                    <el-menu-item index="/manage/picp">发布图集</el-menu-item>
                    <el-menu-item index="/manage/picm">管理图集</el-menu-item>
                    </el-menu-item-group>
                </el-submenu>
                <el-submenu index="author-manage">
                    <template slot="title">
                    <span>个人管理</span>
                    </template>
                    <el-menu-item-group>
                    <el-menu-item index="/manage/picp">更改个人信息</el-menu-item>
                    <el-menu-item index="/manage/picp">更改个人信息</el-menu-item>
                    <el-menu-item index="/manage/picp">更改个人信息</el-menu-item>
                    </el-menu-item-group>
                </el-submenu>
            </el-menu>
        </el-col>
    </el-row>
</template>

<script>
export default {
    name:'navBar',
    data(){
        return {

        }
    }
}
</script>

<style scoped>
    .el-menu-item{
        min-width: 155px!important;
    }
</style>
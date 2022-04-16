<template>
    <div class="activate">
        <div class="tags-body">
            <div class="tags-in">
                <router-view></router-view>
            </div>
        </div>
        <SideBar/>
    </div>
</template>

<script>
import SideBar from '@/components/SideBar.vue'

export default {
    name:'label-item',
    data(){
        return {
        }
    },
    components:{
        SideBar
    },
}
</script>

<style lang="less" scoped>
    .activate{
        margin-top: 15px;
    }
    .tags-body{
        width: 100%;
        margin-left: -25em;
        float: right;
    }
    .tags-in{
        margin-left: 240px;
    }
</style>
<template>
    <div class="activate">
        <div class="category-body">
            <div class="category-in">
                <router-view></router-view>
            </div>
        </div>
        <SideBar/>
    </div>
</template>

<script>
import SideBar from '@/components/SideBar.vue'

export default {
    name:"category-item",
    data(){
        return {

        }
    },
    components:{
        SideBar,
    },
    mounted(){
    },
    methods:{
    }

}
</script>

<style lang="less" scoped>
    .activate{
        margin-top: 15px;
    }
    .category-body{
        width: 100%;
        margin-left: -25em;
        float: right;
    }
    .category-in{
        margin-left: 250px;
    }
</style>
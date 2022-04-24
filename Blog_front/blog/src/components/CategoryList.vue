<template>
    <div>
        <div class="header">
            <h3>
                CategoryList
            </h3>
        </div>
        <div class="tag-title" v-if="show">
            <span>
                目前共计{{total}}个分类
            </span>
        </div>
        <div class="body">
            <ul class="category-list">
                <li class="category-list-item" v-for="item in categorys" :key="item.id">
                    <a class="category-list-link" href="javascript:void(0)" @click="toCategory(item.id,item.name)">{{item.name}}</a>
                </li>
            </ul>
        </div>
    </div>
</template>
<script>
export default {
    name:"category-item",
    data(){
        return {
            categorys:[],
            total:'',
            show:false,
        }
    },
    mounted(){
        this.getCategory()
    },
    methods:{
        getCategory(){
            this.$get(this.$API.API_GET_CATEGORY
            ).then(res => {
                if (res.code == 200) {
                    this.categorys = res.data;
                    this.total = res.data.length;
                    this.show = true;
                } else {
                    console.log(res.msg);
                }
                
            })
        },
        toCategory(id,category){
            window.sessionStorage.setItem("categoryId",id)
            this.$router.push({
                name:"PostByCategory",
                params:{
                    name:category,
                }
            })
        }
    }

}
</script>

<style lang="less" scoped>
    h3{
        font-weight: 200;
        width: 60%;
        margin: 0 auto;
        padding-bottom: 5px;
        border-bottom: 1px solid #e8ecf1;
    }
    .header,.tag-title{
        text-align: center;
        span{
            font-size: 13px;
            font-weight: 200;
            margin-bottom: 10px;
        }
    }
    ul{
        list-style: none;
        margin-top: 10px;
    }
    ul li{
        list-style: circle;
    }
    .category-list-item{
        margin: 5px 10px;
    }
    a{
        font-size: 16px;
        font-weight: 300;
        position: relative;
        display: inline-block;
    }
    a::after{
        content: "";
        display: block;
        width: 100%;
        height: 0.1px;
        position: absolute;
        left: 0;
        background: #222;
        opacity: 0.2;
        transition: all .3s ease-in-out;
    }
    a:hover::after{
        opacity: 1;
    }
</style>
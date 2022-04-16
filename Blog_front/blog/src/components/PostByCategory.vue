<template>
    <div>
        <h3>
            当前分类：{{name}}
        </h3>
        <div class="divide"></div>
        <div class="post-li" v-if="hasPost">
            <ul>
                <li v-for="item in posts" :key="item.id" class="item">
                    <div class="post-item">
                        <div class="post-title">
                            <a :href="'/posts/'+item.id"> {{item.title}} </a>
                        </div>
                        <div class="post-desc">
                            <span class="iconfont">&#xe74f;</span>
                            <span>{{item.author}}</span>
                            <span class="four-right">{{item.time}}</span>
                            <span class="iconfont">&#xe645;</span>
                            <span>阅读:{{item.read_counts}}</span>
                            <span class="iconfont">&#xe6ad;</span>
                            <span>评论:{{item.comment_counts}}</span>
                            <span class="iconfont">&#xe600;</span>
                            <span>喜欢:{{item.like_counts}}</span>
                        </div>
                        <div class="clear"></div>
                    </div>
                </li>
            </ul>
        </div>
        <div v-else>
            <el-empty description="该分类下暂无博客"></el-empty>
        </div>
    </div>
</template>

<script>

export default {
    name:'labels-item',
    data(){
        return {
            name:this.$route.params.name,
            posts:[],
            hasPost:true,
        }
    },
    mounted(){
        this.getPostByLabel()
    },
    methods:{
        getPostByLabel(){
            this.$get(this.$API.API_GET_POST_BY_CATEGORY,{
                id:window.sessionStorage.getItem('categoryId'),
            }).then(res => {
                if (res.code == 200) {
                    this.posts = res.data
                    this.hasPost = true
                    if (this.posts.length == 0) {
                        this.hasPost = false
                    }
                }
            })
        }
    }
    
    
}
</script>

<style scoped lang="less">
  h3{
    font-size: 18px;
    font-weight: 200;
    margin-bottom: 7px;
    text-align: left;
  }
  .divide{
    /* width: 80%; */
    border-bottom: 1px solid #e8ecf1;
    margin-bottom: 8px;
  }
  li{
    list-style: none;
  }
  .post-item{
    margin-bottom: 4px;
    padding-bottom: 5px;
    border-bottom: 1px solid #e8ecf1;
    a{
      display: inline-block;
      font-size: 16px;
      font-weight: 200;
    }
    a:hover{
        color: #456795;
    }
  }
  .post-desc{
      float: right;
      font-size: 12px;
      margin-top: 5px;
      font-weight: 200;
      span{
          margin-left: 3px;
          text-align: center;
          vertical-align: middle;
      }
      .iconfont{
          margin-left: 0px;
          font-size: 12px;
          vertical-align: middle;
          margin-left: 5px;
      }
      .four-right{
          margin-right: 4px;
      }
  }
  .clear{
      clear: both;
  }


</style>
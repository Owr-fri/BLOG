<template>
    <div class="home">
        <Header/>
        <div class="content">
            <div class="warp">
                <h3 class="title">{{title}}</h3>
                <div class="summary" v-show="summary.length!=0">
                    {{summary}}
                </div>
                <div class="imglist">
                    <el-image 
                        v-for="item in img"
                        :key="item.id"
                        :src="$API.BASE_SERVER_URL+item.img"
                        :preview-src-list="srcList"
                        lazy
                        class="img-item"
                    >
                    </el-image>
                </div>
            </div>
            <div class="sider" v-show="show">
                <div class="cover"></div>
                <a href="/" class="avator">
                    <img src="@/common/images/71962138_p0.png" alt="" style="width:100%;border-radius:50%">
                </a>
                <div class="author-desc">
                    <span>Owr</span>
                    <span class="zhanzhang">站长</span>
                </div>
                <div class="recommend">
                    <h3 class="recommend-title">
                        <span>推荐</span>
                    </h3>
                    <div v-for="item in recommendList" :key="item.id" class="img-card">
                        <a :href="'/picture/'+item.title">
                          <el-image
                          :src="$API.BASE_SERVER_URL+item.img"
                          fit="cover"
                          class="picture-cover">
                         </el-image>
                        </a>
                        <span class="picture-title">{{/\d*年\d*月\d*日/.exec(item.title)[0]}}</span>
                    </div>  
                </div>
            </div>
            <div class="pre-next">
              <div>
                <a :href="'/picture/'+prev.title" v-if="prev.id!=-1">上一个</a>
              </div>
              <div>
                <a :href="'/picture/'+next.title" v-if="next.id!=-1">下一个</a>
              </div>
            </div>
            <div class="entry-copyright">
              <span>
                图片均来源于网络,若有侵权请联系
              </span>
            </div>
        </div>
        <Footer/>
    </div>
</template>

<script>
import Header from '@/components/Header.vue'
import Footer from '@/components/Footer.vue'

export default {
    name:'index',
    components:{
        Header,
        Footer,
    },
    data(){
        return {
            img:[],
            summary:'',
            title:'',
            srcList:[],
            recommendList:[],
            prev:'',
            next:'',
            show:false,
        }
    },

    mounted(){
        window.scrollTo(0,0);
        this.getPictureDesc()
        this.getRecommend()
        this.show = true;
    },

    methods:{
        getPictureDesc(){
            let title = this.$route.params["title"]
            this.$get(this.$API.API_GET_PICTURE_DESC,{
                'title':title
            }).then(res => {
                this.img = res.data.imglist;
                let _srcList = []
                res.data.imglist.forEach(i => {
                    _srcList.push(this.$API.BASE_SERVER_URL+i.img)
                });
                this.srcList = _srcList
                this.summary = res.data.summary;
                this.title = /\d*年\d*月\d*日/.exec(res.data.title)[0];
                this.prev = res.data.prev;
                this.next = res.data.next; 
            })
        },
        getRecommend(){
            let title = this.$route.params["title"]
            this.$get(this.$API.API_GET_PICTURE_RECOMMEND,{
                'title':title
            }).then(res => {
                this.recommendList = res.data
            })
        },
    }
}
</script>

<style scoped lang="less">
  .home{
    margin: 0px auto;
    width: 920px;
  }
  .title{
    font-size: 18px;
    font-weight: 400;
    color: #464a4a;
    margin-bottom: 10px;
  }
  .warp{
    margin-top: 10px;
    padding: 10px 15px;
    min-height: 430px;
    width: 640px;
    border: 1px solid #e8ecf1;
    border-radius: 5px;
    box-shadow: 0 0 8px rgba(0,0,0,.2);
  }
  .content{
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
  }
  .summary{
    font-size: 13px;
    font-weight: 200;
    background: #f8f8f8;
    border-radius: 5px;
    padding: 10px 15px;
  }
  .imglist{
    margin-top: 10px;
  }
  .img-item{
    margin: 5px 0;
    max-width: 100%;
  }
  /deep/ .el-image__preview {
    cursor: zoom-in;
  }
  .sider{
    border-radius: 5px;
    width: 230px;
    height: 480px;
    margin: 10px 0 0 15px;
    box-shadow: 0 0 8px rgba(0,0,0,.2);
    position: sticky;
    top: 10px;
  }
  .sider {
    animation: slide-in-bottom 1s cubic-bezier(0.250, 0.460, 0.450, 0.940);
  }
  @keyframes slide-in-bottom {
    0% {
      transform: translateY(1000px);
      opacity: 0;
    }
    100% {
      transform: translateY(0);
      opacity: 1;
    }
  }
  .avator{
    display: block;
    margin: 0 auto;
    height: 64px;
    width: 64px;
    margin-top: -31px;
    
    img{
        background: #fff;
        padding: 1px;
        width: 100%;
    }
  }
  .cover{
    background: #b4b4b466;
    position: relative;
    border-radius: 5px 5px 0 0;
    height: 80px;
    z-index: -1;
  }
  .author-desc{
    text-align: center;
    margin-top: 7px;
    font-weight: 400;
    font-size: 16px;
    padding-bottom: 20px;
    border-bottom: 1px solid #e8ecf1;
    span{
        display: block;
    }
    .zhanzhang{
        font-weight: 200;
        font-size: 12px;
    }
  }
  .recommend-title{
    margin: 10px 0 5px 10px;
    font-size: 12px;
    font-weight: 400;
    position: relative;
    span{
        padding-left: 7px;
    }
  }
  .recommend-title::before{
    position: absolute;
    left: 0;
    top: 2px;
    width: 2px;
    height: 80%;
    content: "";
    border-radius: 3px;
    background-color: #3f3fdfd9;
    vertical-align: middle;
  }
  .picture-cover{
    width: 105px;
    height: 70px;
    display: inline-block;
    border-radius: 5px;
    margin-left: 7px;
    margin-top: 1px;
  }
  .img-card{
    display: inline-block;
  }
  .picture-title{
    margin-top: 1px;
    font-size: 12px;
    font-weight: 200;
    display: block;
    text-align: center;
  }
  .entry-copyright{
    margin: 11px 0 15px 0;
    border-radius: 5px;
    width: 640px;
    box-shadow: 0 0 8px rgba(0,0,0,.2);
    padding: 10px 15px;
    min-height: 35px;
    vertical-align: middle;
    
    span{
      font-size: 13px;
      font-weight: 300;
      line-height: 35px;
    }
  }
  .pre-next{
    margin-top: 4px;
    width: 670px;
    display: flex;
    justify-content: space-between;
    font-size: 12px;
    font-weight: 200;
  }
  .el-image{
    display: block;
  }
</style>
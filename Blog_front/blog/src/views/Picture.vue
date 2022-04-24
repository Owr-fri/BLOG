<template>
    <div class="activate">
        <div class="picture-body">
            <div class="picture-in">
                <div class="picture-header">
                    <h3>
                        Picture
                    </h3>
                </div>
                <div class="picture-title">
                    <span v-if="show">
                        目前共计 {{pictures.length}} 个图集
                    </span>
                </div>
                
                <div class="picture-body">
                    <a href="javascript:void(0)" v-for="(item,index) in pictures" :key="index" @click="toPicture(item.title)">
                        <div 
                          class="img-card"
                          :style="{backgroundImage:'url('+item.img+')',backgroundSize: 'cover',
                                  backgroundPosition: 'center center',backgroundRepeat: 'no-repeat'}"
                          v-lazy="item"
                        >
                        </div>
                        <div class="img-card-title">
                            {{/\d*年\d*月\d*日/.exec(item.title)[0]}}
                        </div>
                    </a>
                </div>
                
            </div>
        </div>
        <SideBar/>
        <div class="clear"></div>
    </div>
</template>

<script>
import SideBar from '@/components/SideBar.vue'

export default {
    name:"picture-item",
    data(){
        return {
            pictures:[],
            show:false,
        }
    },
    components:{
        SideBar,
    },
    mounted(){
        this.getPictures()
    },
    methods:{
        getPictures(){
            this.$get(this.$API.API_GET_PICTURES
            ).then(res => {
                if (res.code==200) {
                    this.pictures = res.data;
                    this.show = true;
                }
            })
        },
        toPicture(title){
            this.$router.push({
                name:"PicturePage",
                params:{"title":title}
            })
        }
    }

}
</script>

<style lang="less" scoped>
    .activate{
        margin-top: 15px;
    }
    .picture-body{
        width: 100%;
        margin-left: -25em;
        float: right;
        a{
            display: inline-flex;
            margin: 4px 5px;
            height: 155px;
            width: 210px;
            position: relative;
            transition: all .2s ease-in-out;
        }
        a:hover{
            .img-card-title{
                background: rgba(0,0,0,0);
                transition: all .2s ease-in-out;
            }
        }
    }
    .picture-in{
        margin-left: 230px;
    }
    .picture-header,.picture-title{
        text-align: center;
        h3{
            font-weight: 200;
            width: 60%;
            margin: 0 auto;
            padding-bottom: 5px;
            border-bottom: 1px solid #e8ecf1;
        }
        span{
            font-size: 13px;
            font-weight: 200;
            margin-bottom: 10px;
        }
    }
    .img-card{
        display: inline-block;
        height: 100%;
        width: 100%;
        border-radius: 5px;
        transition: filter .2s ease-in-out;
        box-shadow: 0 0 8px rgba(0,0,0,.2);
        overflow: hidden;
        -webkit-box-shadow: 0 0 8px rgba(0,0,0,.175);
    }
    .img-card {
        animation: fade-in-bck 1s cubic-bezier(0.390, 0.575, 0.565, 1.000) both;
    }
    @keyframes fade-in-bck {
      0% {
        transform: translateZ(80px);
        opacity: 0;
      }
      100% {
        transform: translateZ(0);
        opacity: 1;
      }
    }
    .img-card:hover{
        filter: brightness(1.1);
    }
    .clear{
        clear: both;
    }
    .img-card-title{
        width: calc(100% - 24px);
        height: 22px;
        background: rgba(0,0,0,.2);
        position: absolute;
        bottom: 0;
        border-radius: 0 0 5px 5px;
        padding: 0 12px;
        font-size: 12px;
        font-weight: 400;
        letter-spacing: .025rem;
        color: #fafafa;
        text-shadow: 0 2px 6px rgb(0 0 0 / 20%);
        text-overflow: ellipsis;
        overflow: hidden;
        white-space: nowrap;
        line-height: 22px;
        z-index: 10;
    }

</style>
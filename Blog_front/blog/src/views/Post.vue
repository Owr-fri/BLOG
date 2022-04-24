<template>
    <div class="home">
        <Header class="header"/>
        <div class="post-content">
            <h1>{{ title }}</h1>
            <div class="content">
                <div class="content-html">
                    <mavon-editor
                        class="md"
                        ref="md"
                        :value="content"
                        :subfield="false"
                        :defaultOpen="'preview'"
                        :toolbarsFlag="false"
                        :shortCut='false'
                        :editable="false"
                        :ishljs="true"
                        @change="dataChange"
                    />
                </div>
                <div class="side-nav">
                    <div v-for="(item,index) in alink" :key="index">
                        <a href="javascript:void(0);" class="nav-link" @click="to(item.id)">
                            {{index+1}}.{{item.name}}
                        </a>
                    </div> 
                </div>
            </div>  
            <div class="divide"></div>
            <div class="desc">
                <p>作者:&nbsp; {{ author }}</p>
                <p>出处:&nbsp; <a :href="href">{{href}}</a></p>
                <p>未经授权不得转载</p>
            </div>
            <div class="tags">
                <div class="category">
                    <span class="iconfont">&#xe64b;</span>
                    <span>分类:</span>
                    <a href='javascript:void(0)' @click="toCategory(category.id,category.name)">
                        {{ category.name }}
                    </a>
                </div>
                <div class="label">
                    <span class="iconfont">&#xe886;</span>
                    <span>标签:</span>
                    <a href='javascript:void(0)' v-for="(item,index) in label" :key=index @click="toLabel(item.id,item.name)">
                        #{{item.name}}
                    </a>
                </div>
                <div class="time">
                    <span class="iconfont">&#xe619;</span>
                    <span>时间:</span>
                    <span> &nbsp;{{publishTime}} </span>
                </div>
            </div>
            <div class="diggit">
                <div class="dianzan" @click="dianzan" :style="dianzanStyle">
                    <span class="iconfont">&#xe600;</span>
                </div>
                <div class="cai" @click="cai" :style="caiStyle">
                    <span class="iconfont">&#xea0b;</span>
                </div>
            </div>
            <div class="clear"></div>
            <div class="post_next_prev">
                <div class="prev" v-if="prev.id!=-1">
                    <span class="prev_span">上一篇:</span>
                    <a :href=prev.id > {{prev.title}} </a>
                </div>
                <div class="next" v-if="next.id!=-1">
                    <span class="next_span" >下一篇:</span>
                    <a :href=next.id> {{next.title}} </a>
                </div>
            </div>
            <div class="divide_all"></div>
            <div class="other">
                <span>点赞({{like_counts}})</span>
                <span class="read-item">阅读({{read_counts}})</span>
                <span>评论({{comment_counts}})</span>
            </div>
            <div class="clear"></div>
        </div>

        <div class="comment">
            评论
        </div>
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

    data(){
        return {
            title:'',
            content:'',
            category:'',
            publishTime:'',
            like_counts:'',
            read_counts:'',
            comment_counts:'',
            author:'',
            label:[],
            href:location.origin+location.pathname,
            dianzanStyle:'',
            caiStyle:'',
            dianzanClicked:false,
            caiClicked:false,
            isClicked:false,
            next:'',
            prev:'',
            alink:[],
        }
    },

    mounted(){
        this.getPost()
    },
    

    methods:{
        dataChange(value,render){
            let reg = /<h.?><a id="(.*?)"><.a>(.*?)<.?h.?>/g
            if (render.match(reg)) {
                render.match(reg).forEach(i => {
                    let id = i.match(/id="(.*?)"/)[1]
                    let name = i.match(/<.?a>(.*?)<.?h.?>/)[1]
                    this.alink.push({
                        "id":id,
                        "name":name
                    })
                });
            }
        },
        
        getPost(){
            this.$get(this.$API.API_GET_POST,{
                id:this.$route.params["p"]
            }).then(res => {
                if (res.code == 200) {
                    this.id = res.data.id
                    this.title = res.data.title
                    this.content = res.data.content
                    this.author = res.data.author
                    this.category = res.data.category
                    this.label = res.data.label
                    this.publishTime = res.data.publishTime
                    this.next = res.data.next
                    this.prev = res.data.prev
                    this.read_counts = res.data.read_counts
                    this.comment_counts = res.data.comment_counts
                    this.like_counts = res.data.like_counts
                } else {
                    console.log(res.msg)
                }
            })
        },
        dianzan(){
            if (this.caiClicked){
                return
            }
            if (this.dianzanClicked) {
                this.dianzanStyle = '';
                this.dianzanClicked = false;
                this.like_counts -= 1;

                this.$post(this.$API.API_LIKE,{
                    id:this.id,
                    counts:this.like_counts,
                }).then(res => {
                    console.log(res)
                })
                return
            }
            this.dianzanStyle = 'background: #3d615e;color: #f8f8f8;'
            this.dianzanClicked = true;
            this.like_counts += 1;

            this.$post(this.$API.API_LIKE,{
                id:this.id,
                counts:this.like_counts,
            }).then(res => {
                console.log(res)
            })
        },
        cai(){
            if (this.dianzanClicked){
                return
            }
            if (this.caiClicked) {
                this.caiStyle = '';
                this.caiClicked = false;
                return
            }
            this.caiStyle = 'background: #3d615e;color: #f8f8f8;'
            this.caiClicked = true;
        },
        toLabel(id,label){
            window.sessionStorage.setItem("labelId",id)
            this.$router.push({
                name:"PostByLabel",
                params:{
                    name:label,
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
        },
        to(url){
            document.querySelector('#' + url).scrollIntoView(true);
        }
    }
}
</script>

<style lang="less" scoped>
    .home{
        margin: 0px auto;
        width: 920px;
        min-height: 100%;
    }
    .footer{
        margin: 0px auto;
        width: 920px;
        height:45px;
        bottom:0px;
    }

    .post-content{
        margin-top: 15px;
        min-height: calc(90vh);
        width: 100%;
    }
    h1{
        margin-bottom: 10px;
        font-size: 21px;
        color: #464a4a;
    }
    .divide{
        display: block;
        width: 60%;
        margin: 20px 0 20px 97px;
        // margin: 20px auto;
        // width: 70%;
        border-bottom: 1px solid #e8ecf1;
    }
    .divide_all{
        width: 100%;
        border-bottom: 1px solid #e8ecf1;
    }
    .clear{
        clear: both;
    }
    .other{
        float: right;
        font-size: 12px;
        font-weight: 200;
        color: #464a4a;
        span{
            margin-left: 3px;
        }
    }
    .post_next_prev{
        font-size: 12px;
        font-weight: 200;
        margin-bottom: 5px;
        span{
            line-height: 1.5;
        }
        .prev_span::before{
            content: "\00AB";
        }
        .next_span::before{
            content: "\00bb";
        }
        a{
            position: relative;
            color: #456795;
            margin-left: 5px;
            display: inline-block;
        }
        a::after{
            content: "";
            display: block;
            width: 100%;
            height: 0.1px;
            position: absolute;
            left: 0;
            background: #456795;
            transform: scaleX(0);
            transform-origin: left;
            transition: all .3s ease-in-out;
        }
        a:hover::after{
            transform: scaleX(1);
        }
    }
    .diggit{
        margin: 20px 0 5px 0;
        float: right;
        cursor: pointer;
        .dig-dianzan,.dig-cai{
            font-size: 14px;
            margin-left: 2px;
        }
        .iconfont{
            font-size: 16px;
            font-weight: 200;
        }
        .dianzan,.cai{
            color: #464a4a;
            display: inline-block;
            width: 60px;
            text-align: center;
            background: #f8f8f8;
            padding: 4px 3px 4px 0;
            border-radius: 5px;
            transition: all .3s ease;
        }
        .dianzan{
            margin-right: 10px;
        }
        .dianzan:hover,.cai:hover{
            background: #3d615e;
            color: #f8f8f8;
            transition: all .3s ease;
        }

    }
    .desc{
        background: #f8f8f8;
        border-radius: 3px;
        margin: 0 auto;
        margin-bottom: 10px;
        padding: 12px 24px 12px 20px;
        border-left: 4px solid #2b6964;

        p{
            font-size: 13px;
            color: #3d615e;
            line-height: 1.5;
            font-weight: 200;
        }
        a{
            display: inline-block;
            position: relative
        }
        a::after{
            content: "";
            display: block;
            width: 100%;
            height: 0.1px;
            position: absolute;
            left: 0;
            background: #3d615e;
            transform: scaleX(0);
            transform-origin: left;
            transition: all .3s ease-in-out;
        }
        a:hover::after{
            height: 0.1px;
            transform: scaleX(1);
        }

    }
    .tags{
        margin-top: 15px;
        color: #464a4a;
        opacity: 0.8;
        font-weight: 200;
        line-height: 1;
        vertical-align: middle;
        font-size: 12px;

        .iconfont{
            font-size: 12px;
            margin: 0 5px;
        }

        a{
            font-weight: 100;
            display: inline-block;
            margin-left: 7px;
            color: #464a4a;
            background: #f8f8f8;
            padding: 4px 6px;
            border-radius: 3px;
        }

        a:hover{
            background: #3d615e;
            color: white;
        }
        
        .category,.label{
            margin-bottom: 5px;
        }
    }
    .side-nav{
        position: sticky;
        margin-left: 15px;
        height: 200px;
        top: 20px;
        overflow: hidden;
        .nav-link{
            display: inline-block;
            font-size: 12px;
            font-weight: 200;
            color: black;
            line-height: 1.5;
            margin-top: 4px;
            vertical-align: middle;
        }
    }
    .content{
        width: 100%;
        display: flex;
    }
    .content-html{
        min-height: calc(50vh);
        // border-right: 1px solid #e8ecf1;
        // border-left: 1px solid #e8ecf1;
        // padding: 0 10px;
        padding: 0 10px 0 0;
        border-right: 1px solid #e8ecf1;
        width: 80%;

        /deep/ h1{
            font-size: 21px;
            color: #464a4a;
        }
        /deep/ h2{
            font-size: 20px;
            margin-bottom: 10px;
            color: #464a4a;
        }
        /deep/ h3{
            margin: 10px 0px;
            font-size: 18px;
            color: #464a4a;
            cursor: pointer;
            display: inline-block;
        }
        /deep/ img{
            overflow: hidden;
            max-width: 720px;
            display: block;
            margin: 5px 0;
            border-radius: 3px;
            box-shadow: 1px 1px 2px #5c5c5c94;
            width: 100%;
        }
        /deep/ p{
            font-size: 14px;
            font-weight: 200;
            line-height: 1.5;
        }
        /deep/ h3::after{
            content:'';
        }

        /deep/ h3:hover::after{
            content: "#";
            color: #456795;
            height: 0px;
            position: absolute;
            animation: fade-in 0.5s cubic-bezier(0.390, 0.575, 0.565, 1.000) both;
        }
        @keyframes fade-in {
            0% {
                opacity: 0;
            }
            100% {
                opacity: 1;
            }
        }
        /deep/ p a{
            color: #456795;
            text-decoration: none;
        }

        /deep/ p a::after{
            content: "";
            display: block;
            width: 100%;
            height: 1px;
            position: absolute;
            left: 0;
            bottom: -2px;
            background: #456795;
            transform: scaleX(0);
            transform-origin: left;
            transition: all .3s ease-in-out;
        }

        /deep/ p a:hover::after{
            transform: scaleX(1);
        }

        /deep/ p a{
            margin-left: 5px;
            display: inline-block;
            position: relative;
            text-align: center;
        }
    }
</style>
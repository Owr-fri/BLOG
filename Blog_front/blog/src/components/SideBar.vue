<template>
    <div class="sidebar">
        <img src="@/common/images/71962138_p0.png" alt="" class="avatar">
        <!-- <span class="iconfont">&#xea0a;</span> -->
        <div class="authorinfo">
            <span>Owr</span>
        </div>
        <div class="blog-state">
            <nav>
                <div class="blog-state-item blog-state-posts">
                    <a href="/blog" class="state-item">
                    <span class="state-item-count">{{ posts_counts }}</span>
                    <span class="state-item-name">博客</span>
                    </a>
                </div>
                <div class="blog-state-item blog-state-p">
                    <a href="/p" class="state-item">
                    <span class="state-item-count">{{ p_conts }}</span>
                    <span class="state-item-name">标签</span>
                    </a>
                </div>
                <div class="blog-state-item blog-state-pictures">
                    <a href="/picture" class="state-item">
                    <span class="state-item-count">{{ picture_counts }}</span>
                    <span class="state-item-name">图集</span>
                    </a>
                </div>
            </nav>
        </div>
        <div class="link-of-author">
            <span class="link-of-author-item link-github">
                <a href="https://github.com/Owr-fri" target="_blank">
                    <span class="iconfont">&#xea0a;</span>
                    Github
                </a>
            </span>
            <span class="link-of-author-item link-email">
                <a href="mailto:431306642@qq.com" target="_blank">
                    <span class="iconfont">&#xe612;</span>
                    Email
                </a>
            </span>
        </div>
        <div class="search-bar">
            <h3 class="search-title">
                搜索
            </h3>
            <div class="search-item">
                <input class="search-in" type="text">
                <input type="button" class="search-but" value="查看"> 
            </div>
        </div>
        <div class="hotposts">
            <h3 class="hotposts-title">
                热门博客
            </h3>
            <div class="hotposts-item">
                <ul>
                    <li v-for="(item,index) in hotposts" :key="index" class="hotpost">
                        <a href="/" class="hotpost-title">{{ index+1 }}. {{ item.title }}</a>
                        <div class="hotpost-summary">
                            <p class="summary-content">{{ item.summary }}</p>
                        </div>
                        <div class="hotpost-author">
                            --{{ item.author }}
                        </div>
                    </li>
                </ul>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name:"sideBar",
    data(){
        return {
            posts_counts:45,
            p_conts:23,
            picture_counts:11,
            hotposts:[
                {
                    title:"Life Long Learning",
                    summary:"Life long learning又可以叫做终身学习；对于人类自身而言，我们每次都是用同一个脑来学习机器学习的每一堂课，每次的作业也都需要训练不同的神经网络，那么我们可不可以每次作业都使用同一个神经网络呢？ life long learning可简称为LLL，也可被称作Continuous Learning, Never Ending Learning, Incremental Learning",
                    author:"Owr"
                },
                {
                    title:"Meta Learning",
                    summary:"本文主要叙述了meta learning的核心思想，对比了machine learning和meta learning的三个步骤；接着介绍了meta learning一般会用到的数据集Omniglot；除了meta learning，本文还讲了transfer learning的其他两个技术：MAML和Reptile。 IntroductionMeta learning可以让机器学习如何去le",
                    author:"Owr",
                },
                {
                    title:"Transfer Learning",
                    summary:"本文主要针对source和target data的不同情况，介绍了几种主要的transfer learning的方式，包括Fine-tuning、Multitask learning、domain-adversarial training、zero-shot learning。 如果现在没有和我们任务直接相关的数据，比如我们要做的任务是猫狗分类，很可能手头只有elephant和tiger的数据",
                    author:"Owr",
                },
            ],
        }
    }
}
</script>

<style scoped>
    .avatar{
        max-width: 100%;
        border-radius: 5px;
        box-shadow: 2px 2px 5px #2b6964;
    }
    .sidebar{
        width: 200px;
        padding-right: 15px;
        border-right: 1px solid #e8ecf1;
    }
    .authorinfo{
        margin-top: 7px;
        width: 100%;
        text-align: center;
        /* margin-left: -5px; */
    }
    .authorinfo span{
        font-size: 20px;
        color: #3d615e;
        font-family: Georgia;
    }
    .blog-state-item{
        border-left: 1px solid #e8ecf1;
        display: inline-block;
        padding: 0 15px;
    }
    .blog-state-posts{
        border-left: none;
    }
    .state-item-count{
        display: block;
        text-align: center;
    }
    .blog-state{
        white-space: nowrap;
        padding-top: 12px;
        margin-left: 11px;
    }
    .state-item{
        line-height: 1.5;
    }
    .state-item:hover{
        color: #3fc9be;
    }
    .state-item-count{
        font-size: 12px;
    }
    .state-item-name{
        font-size: 14px;
    }
    .link-of-author a{
        display: inline-block;
        font-size: 11px;
        vertical-align: middle;
        margin-left: 10px;
        line-height: 1.2;
        border-bottom: 1px solid #e8ecf1;
    }
    .link-of-author a:hover{
        color: #3fc9be;
    }
    .link-of-author a::before{
        display: inline-block;
        vertical-align: middle;
        margin-right: 5px;
        content: "";
        width: 5px;
        height: 5px;
        border-radius: 50%;
        background: #606266;
    }
    .link-of-author{
        margin-top: 15px;
        text-align: center;
    }
    .iconfont{
        font-size: 13px;
    }
    .search-in{
        width: 60%;
        margin-right: 4px;
        border: 1px solid #eef2f8;
        vertical-align: middle;
        height: 26px;
        font-size: 14px;
        font-weight: 100;
        border-radius: 4px;
        outline: none;
        line-height: 30px;
        color: #606266;
    }
    .search-but{
        width: 30%;
        height: 30px;
        border: 1px solid #eef2f8;
        border-radius: 4px;
        background-color: transparent;
        vertical-align: middle;
        color: #606266;
        cursor: pointer;
    }
    .search-but:hover{
        color: #b5ebe6;
        border: 1px solid #b5ebe6;
        transition: all .3s;
    }
    .search-title,.hotposts-title{
        vertical-align: middle;
        color: #798a8b;
        font-weight: inherit;
        margin: 30px 0 20px 0;
        font-size: 16px;
        padding-left: 10px;
        border-left: 4px solid #596172;
        border-radius: 4px;
    }
    .hotpost{
        border-top: 1px solid #e8ecf1;
        padding-top: 10px;
        margin-bottom: 15px;
        list-style: none;
    }
    .hotposts-item ul{
        padding: 0px;
    }
    .hotpost-title{
        font-weight: 300;
        font-size: 14px;
        word-wrap: break-word;
        word-break: break-all;
        color: #596172;
    }
    .hotpost-title:hover{
        color: #177e77;
    }
    .hotpost-summary{
        padding: 3px 0;
        margin: 7px 0 0 5px;
        font-size: 11px;
        background-color: #f8f8f8;
        border-radius: 5px;
    }
    .summary-content{
        font-weight: 300;
        margin: 5px 10px;
        display: -webkit-box;
        color: #505560;
        overflow: hidden;  
        text-overflow:ellipsis;
        -webkit-box-orient: vertical;
        -webkit-line-clamp:3;
        word-wrap: break-word;
        word-break: break-all;
    }
    .hotpost-author{
        text-align: right;
        font-size: 12px;
        font-weight: 300;
        color: #3d615e;
        margin-top: 4px;
    }
    .hotposts{
        border-bottom: 1px solid #e8ecf1;
    }
</style>
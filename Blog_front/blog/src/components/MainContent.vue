<template>
    <div class="main-content">
        <div class="posts">
            <ul class="posts-ul">
                <li v-for="(item,index) in posts" :key="index" class="post-item">
                    <div class="post-title">
                        <a href="" class="post-link">
                            <span>
                                {{ item.title }}
                            </span>
                        </a>
                    </div>
                    <div class="post-meta">
                        <span class="post-time">
                            <span class="iconfont">&#xe8b4;</span>
                            <span>发布于 </span>
                            <time>{{ item.time }}</time>
                        </span>
                        <span class="post-meta-separate"></span>
                        <span class="post-cate">
                            <span class="iconfont">&#xe7b8;</span>
                            <span>分类于 </span>
                            <a href="">{{ item.category }}</a>
                        </span>
                    </div>
                    <div class="post-main">
                        <div class="post-content">
                            {{ item.content }}
                            <a href="" class="read-desc">阅读全文</a>
                        </div>
                    </div>
                    <div class="post-desc">
                        <span class="post-author">
                            posted@{{ item.author }}
                        </span>
                        &nbsp;&nbsp;&nbsp;
                        <span class="iconfont">&#xe645;</span>
                        <span class="post-read">
                            阅读({{item.read}})
                        </span>
                        &nbsp;
                        <span class="iconfont">&#xe6ad;</span>
                        <span class="post-comment">
                            评论({{item.comment}})
                        </span>
                        &nbsp;
                        <span class="iconfont">&#xe600;</span>
                        <span class="post-like">
                            ({{item.like}})
                        </span>
                    </div>
                    <div class="separate"></div>
                </li>
            </ul>
        </div>
    </div>    
</template>

<script>
export default {
    name:'mainContent',
    data(){
        return {
            posts:[
                {
                    title:'Meta Learning',
                    content:'本文主要叙述了meta learning的核心思想，对比了machine learning和meta learning的三个步骤；接着介绍了meta learning一般会用到的数据集Omniglot；除了meta learning，本文还讲了transfer learning的其他两个技术：MAML和Reptile。 IntroductionMeta learning可以让机器学习如何去le',
                    time:'2020-07-22',
                    author:'Owr',
                    comment:'12',
                    like:'2',
                    category:'ML-notes',
                    read:'37',
                },
                {
                    title:'Transfer Learning',
                    content:'本文主要针对source和target data的不同情况，介绍了几种主要的transfer learning的方式，包括Fine-tuning、Multitask learning、domain-adversarial training、zero-shot learning。 如果现在没有和我们任务直接相关的数据，比如我们要做的任务是猫狗分类，很可能手头只有elephant和tiger的数据',
                    time:'2020-07-20',
                    author:'Owr',
                    comment:'16',
                    like:'8',
                    category:'ML-notes',
                    read:'31',
                },
                {
                    title:'Sequence Labeling Problem',
                    content:'本文主要介绍了几种传统的序列标注方法，包括HMM（隐马尔可夫模型），CRF（条件随机场），Structed perception/SVM。 IntroductionSequence Labeling首先叙述sequence labeling的基本概念，machine的任务就是学习出一个函数f，可以实现sequence X到Y的转换。 现在我们假设X和Y的长度是一样的，输入x1,…,xL，输',
                    time:'2020-07-17',
                    author:'Owr',
                    comment:'23',
                    like:'17',
                    category:'ML-notes',
                    read:'65',
                },
                {
                    title:'Sequence Labeling Problem',
                    content:'本文主要介绍了几种传统的序列标注方法，包括HMM（隐马尔可夫模型），CRF（条件随机场），Structed perception/SVM。 IntroductionSequence Labeling首先叙述sequence labeling的基本概念，machine的任务就是学习出一个函数f，可以实现sequence X到Y的转换。 现在我们假设X和Y的长度是一样的，输入x1,…,xL，输',
                    time:'2020-07-17',
                    author:'Owr',
                    comment:'23',
                    like:'17',
                    category:'ML-notes',
                    read:'65',
                },
                {
                    title:'Sequence Labeling Problem',
                    content:'本文主要介绍了几种传统的序列标注方法，包括HMM（隐马尔可夫模型），CRF（条件随机场），Structed perception/SVM。 IntroductionSequence Labeling首先叙述sequence labeling的基本概念，machine的任务就是学习出一个函数f，可以实现sequence X到Y的转换。 现在我们假设X和Y的长度是一样的，输入x1,…,xL，输',
                    time:'2020-07-17',
                    author:'Owr',
                    comment:'23',
                    like:'17',
                    category:'ML-notes',
                    read:'65',
                },
                {
                    title:'Sequence Labeling Problem',
                    content:'本文主要介绍了几种传统的序列标注方法，包括HMM（隐马尔可夫模型），CRF（条件随机场），Structed perception/SVM。 IntroductionSequence Labeling首先叙述sequence labeling的基本概念，machine的任务就是学习出一个函数f，可以实现sequence X到Y的转换。 现在我们假设X和Y的长度是一样的，输入x1,…,xL，输',
                    time:'2020-07-17',
                    author:'Owr',
                    comment:'23',
                    like:'17',
                    category:'ML-notes',
                    read:'65',
                },
                {
                    title:'Sequence Labeling Problem',
                    content:'本文主要介绍了几种传统的序列标注方法，包括HMM（隐马尔可夫模型），CRF（条件随机场），Structed perception/SVM。 IntroductionSequence Labeling首先叙述sequence labeling的基本概念，machine的任务就是学习出一个函数f，可以实现sequence X到Y的转换。 现在我们假设X和Y的长度是一样的，输入x1,…,xL，输',
                    time:'2020-07-17',
                    author:'Owr',
                    comment:'23',
                    like:'17',
                    category:'ML-notes',
                    read:'65',
                },
                {
                    title:'Sequence Labeling Problem',
                    content:'本文主要介绍了几种传统的序列标注方法，包括HMM（隐马尔可夫模型），CRF（条件随机场），Structed perception/SVM。 IntroductionSequence Labeling首先叙述sequence labeling的基本概念，machine的任务就是学习出一个函数f，可以实现sequence X到Y的转换。 现在我们假设X和Y的长度是一样的，输入x1,…,xL，输',
                    time:'2020-07-17',
                    author:'Owr',
                    comment:'23',
                    like:'17',
                    category:'ML-notes',
                    read:'65',
                },
                {
                    title:'Sequence Labeling Problem',
                    content:'本文主要介绍了几种传统的序列标注方法，包括HMM（隐马尔可夫模型），CRF（条件随机场），Structed perception/SVM。 IntroductionSequence Labeling首先叙述sequence labeling的基本概念，machine的任务就是学习出一个函数f，可以实现sequence X到Y的转换。 现在我们假设X和Y的长度是一样的，输入x1,…,xL，输',
                    time:'2020-07-17',
                    author:'Owr',
                    comment:'23',
                    like:'17',
                    category:'ML-notes',
                    read:'65',
                },
                {
                    title:'Sequence Labeling Problem',
                    content:'本文主要介绍了几种传统的序列标注方法，包括HMM（隐马尔可夫模型），CRF（条件随机场），Structed perception/SVM。 IntroductionSequence Labeling首先叙述sequence labeling的基本概念，machine的任务就是学习出一个函数f，可以实现sequence X到Y的转换。 现在我们假设X和Y的长度是一样的，输入x1,…,xL，输',
                    time:'2020-07-17',
                    author:'Owr',
                    comment:'23',
                    like:'17',
                    category:'ML-notes',
                    read:'65',
                },
            ]
        }
    }
}
</script>

<style scoped> 
    .main-content{
        width: 100%;
        margin-left: -25em;
        float: right;
        
    }
    .posts{
        margin-left: 230px;
        
    }
    .post-item{
        list-style: none;
    }
    .posts-ul{
        padding: 0;
    }
    .post-link{
        font-size: 22px;
        font-weight: 500;
        position: relative;
        display: inline-block;
        color: #596172;
        
    }
    .post-link::before{
        content: "";
        display: block;
        width: 100%;
        height: 1px;
        position: absolute;
        bottom: 0;
        left: 0;
        background-color: #3d615e;
        transform: scaleX(0);
        transition: transform .4s ease-in-out;
    }
    .post-link:hover:before{
        transform: scaleX(1);
    }
    .post-link:hover{
        color: #177e77;
    }
    .post-main{
        margin-top: 5px;
    }
    .post-content{
        font-size: 15px;
        color: #505560;
        font-weight: 300;
        word-break: break-all;
        word-wrap: break-word;
        text-align: justify;
    }
    .post-content a::after{
        content: "\00bb";
    }
    .read-desc{
        display: table;
        margin-top: 15px;
        color: #3d615e;
        font-size: 15px;
        border-bottom: 2px dotted #505560;
        font-weight: 300;
    }
    .read-desc:hover{
        color: #000;
    }
    .separate{
        margin: 20px 0;
        border-bottom: 1px solid #e8ecf1;
    }
    .post-meta-separate{
        border-left: 1px solid #999;
        margin: 0 7px;
    }
    .post-meta{
        margin: 10px 0;
        font-size: 12px;
        color: #999;
        font-weight: 200;
    }
    .post-cate a{
        display: inline-block;
        border-bottom: 1px solid #999;
    }
    .post-cate a:hover{
        color: rgb(0, 0, 0);
        border-bottom: 1px solid rgb(0, 0, 0);
    }
    .post-meta .iconfont,.post-desc .iconfont{
        font-size: 12px;
        margin: 0 3px;
    }
    .post-desc{
        text-align: right;
        margin-top: 10px;
        font-size: 13px;
        font-weight: 200;
        color: #505560;
    }
</style>
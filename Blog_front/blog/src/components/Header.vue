<template>
    <div id="header">
      <div id="title">
        <h1>
          <a>Owr的博客</a>
        </h1>
        <a id="slogan">能者敛其锋芒</a>
      </div>
      <ul>
        <li><a href="/">首页</a></li>
        <li><a href="/blog">博客</a></li>
        <li><a href="/p">标签</a></li>
        <li><a href="/category">分类</a></li>
        <li><a href="/picture">图集</a></li>
        <li><a href="/manage">管理</a></li>
        <li><a href="/login">登录</a></li>
      </ul>
    </div>
</template>
 
<script>
export default {
    name: "Header",
}
</script>
<style>
  #header{ 
    height: 50px;
    font-weight: 300;
    /* border-bottom: 1px solid #eef2f8; */
    border-bottom: 1px solid #e8ecf1;
  }
  #header ul{ 
    position: relative; 
    margin: 0 auto;
    float: right;
    margin-right: 10px;
  }
  #header li{
    float: left;
    margin-right: 0px;
    font-size: 17px;
    width: 50px;
    height: 40px;
    list-style: none;
  }
  #header ul li a{
    line-height: 50px;  
    position: relative;
    text-align: center;
  }
  #title{
    display: inline-block;
  }
  h1{
    margin: 0px;
    color: #3d615e;
    font-family: Georgia;
    float: left;
  }
  #title h1 a{
    line-height: 40px;
    font-size: 22px;
    text-align: center;
  }
  #slogan{
    position: relative;
    text-align: left;
    line-height: 10px;
    bottom: 5px;
    font-size: 10px;
    color: #596172;
    opacity: .8;
  }
  a{
    color: #3d615e;
    text-decoration: none;
    display: block;
    z-index: 200;
    transition: all .3s ease;
  }
  body{
    margin: 0;
    padding: 0;
  }
  #header ul li a:before{
    content: "";
    position: absolute;
    width: 100%;
    height: 3px;
    bottom: 0;
    left: 0;
    background-color: #3fc9be;
    transform: scaleX(0);
    transform-origin: right;
    transition: transform .4s ease;
  }
  #header ul li a:hover:before{
    transform: scaleX(1);
    transform-origin: left;
  }
  #header ul li a:hover{
    color: #3fc9be;
  }
</style>
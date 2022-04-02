<template>
    <div class="home">
        <Header/>
        <div class="page-content">
          <MainContent/>
          <SideBar/>
          <div class="clear"></div>
        </div>
        <ToolBar/>
        <Footer/>
    </div>
</template>

<script>
import Header from '@/components/Header.vue'
import SideBar from '@/components/SideBar.vue'
import MainContent from '@/components/MainContent.vue'
import Footer from '@/components/Footer.vue'
import ToolBar from '@/components/ToolBar.vue'

export default {
    name:'index',
    components:{
        Header,
        SideBar,
        MainContent,
        Footer,
        ToolBar,
    }
}
</script>

<style scoped>
  .home{
    margin: 0px auto;
    width: 940px;
  }
  .page-content{
    margin: 15px 0;
    display: block;
    min-height: calc(100% - 75px);
    max-height: 100%;
  }
  .clear{
    clear: both;
  }
</style>
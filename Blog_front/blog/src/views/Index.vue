<template>
  <div class="home">
    <Header />
    <div class="con">
      <router-view @cleanSearchInput="cleanSearchInput"></router-view>
    </div>
    <SideBar class="sb" ref="sb"/>
    <div class="clear"></div>
    <Footer />
  </div>
</template>

<script>
  import Header from '@/components/Header.vue'
  import Footer from '@/components/Footer.vue'
  import SideBar from '@/components/SideBar.vue'

  export default {
    name: 'index',
    components: {
      Header,
      Footer,
      SideBar,
    },
    methods:{
      cleanSearchInput(){
        this.$refs.sb.state = '';
        this.$refs.sb.searchList = [];
      }
    }
  }
</script>

<style scoped>
  .home {
    margin: 0px auto;
    width: 920px;
  }
  .con {
    width: 100%;
    margin-left: -25em;
    float: right;
  }
  .sb {
    margin-top: 15px;
  }
  .clear {
    clear: both;
  }
</style>
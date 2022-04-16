<template>
    <div>
        <Header/>
        <SideBar/>
        <Footer/>
    </div>
</template>

<script>
import Header from '@/components/Header.vue'
import SideBar from '@/components/SideBar.vue'
import Footer from '@/components/Footer.vue'

export default {
    name:'tags-item',
    data(){
        return {

        }
    },
    components:{
        Header,
        SideBar,
        Footer,
    }
}
</script>
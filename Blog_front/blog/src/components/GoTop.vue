<template>
    <div class="tool-bar">
        <div class="tool-item" v-show="goTopShow" @click="goTop">
            <span class="iconfont">&#xe679;</span>
        </div>
    </div>
</template>

<script>
export default {
    name:'toolBar',
    data(){
        return {
            scrollTop:"",
            goTopShow:false,
        }
    },
    watch: {
        scrollTop() {
            if (this.scrollTop > 400) {
                this.goTopShow = true;
            } else {
                this.goTopShow = false;
            }
        }
    },
    methods: {
        handleScroll() {
            this.scrollTop =
                window.pageYOffset ||
                document.documentElement.scrollTop ||
                document.body.scrollTop;
            if (this.scrollTop > 400) {
                this.goTopShow = true;
            }
        },
        goTop() {
            cancelAnimationFrame(this.timer)
            const self = this
            self.timer = requestAnimationFrame(function fn () {
                const oTop = document.body.scrollTop || document.documentElement.scrollTop
                if (oTop > 0) {
                document.body.scrollTop = document.documentElement.scrollTop = oTop - 60
                self.timer = requestAnimationFrame(fn)
                } else {
                cancelAnimationFrame(self.timer)
                }
            })
        }
    },
    mounted() {
        window.addEventListener("scroll", this.handleScroll);
    },
    destroyed() {
        window.removeEventListener("scroll", this.handleScroll);
    }

}
</script>

<style scoped>
    .tool-bar{
        position: fixed;
        bottom: 50px;
        right: 80px;
        width: 45px;
        height: 45px;
        z-index: 1001;
    }
    .tool-item{
        position: relative;
        width: inherit;
        height: inherit;
        cursor: pointer;
        border-radius: 50%;
        background: #f8f8f8;
        text-align: center;
        vertical-align: middle;
        line-height: 46px;
        color: #596172;
        box-shadow: 2px 2px 4px 0px rgb(0 0 0 / 20%);
    }
</style>
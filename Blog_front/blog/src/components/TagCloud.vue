<template>
    <div class="tag-cloud">
        <div class="tag-header">
            <h3>
                TagCloud
            </h3>
        </div>
        <div class="tag-title">
            <span v-if="show">
                目前共计 {{total}} 个标签
            </span>
        </div>
        <div class="body">
            <table>
                <tbody align="center" valign="center">
                    <tr v-for="(items,index) in labels" :key="index">
                        <td v-for="item in items" :key="item.id">
                            <a href="javascript:void(0)" @click="toLabel(item.id,item.label)">{{item.label}}</a>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script>

export default {
    name:'tag-cloud',
    data(){
        return {
            labels:[],
            total:'',
            show:false,
        }
    },
    mounted(){
        this.getLabels()
    },
    methods:{
        getLabels(){
            this.$get(this.$API.API_GET_LABEL
            ).then(res => {
                if (res.code == 200) {
                    this.total = res.data.length;
                    this.show = true;
                    for (let i = 0; i < Math.ceil(res.data.length/6); i++) {
                        let four = []
                        for (let j = 0; j < 6; j++) {
                            if (res.data[i*6+j]) {
                                 four.push(res.data[i*6+j])
                            }
                        }
                        this.labels.push(four)
                    }
                } else {
                    console.log(res.msg)
                }
            })
        },
        toLabel(id,label){
            window.sessionStorage.setItem("labelId",id)
            this.$router.push({
                name:"PostByLabel",
                params:{
                    name:label,
                }
            })
        }
    }
}
</script>

<style lang="less" scoped>
    .tag-header,.tag-title{
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
    .body{
        margin-top: 10px;
        text-align: center;
    }
    td a{
        display: block;
        padding: 5px;
        font-weight: 200;
        font-size: 12px;
        line-height: 20px;
        text-align: center;
        border: 1px solid #eef2f8;
        border-radius: 4px;
        color: #596172;
    }
    td{
        padding: 5px 10px 5px 0;
    }
    table{
        width: 100%;
    }
    a:hover{
        border: 1px solid #3d615e;
    }
</style>
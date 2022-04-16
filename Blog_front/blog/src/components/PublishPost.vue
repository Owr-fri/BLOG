<template>
    <div class="postp-content">
        <h2 class="content-title">发表博客</h2>
        <div class="title-item">
            <span>标题</span>
            <el-input
                type="text"
                placeholder="请输入内容"
                v-model="title"
                maxlength="50"
                show-word-limit
                size='small'
            >
            </el-input>
        </div>
        <div class="post-desc">
            <div class="category-item">
                <span>分类</span>
                <MulSelect :options="categroy" :isMultiple="false" ref="M1"/>
            </div>
            <div class="divide"> </div>
            <div class="label-item">
                <span>标签</span>
                <MulSelect :options="label" ref="M2"/>
            </div>
        </div>
        <div class="post-summary">
            <h4>摘要</h4>
            <el-input
                type="textarea"
                maxlength=100
                show-word-limit
                :autosize="{ minRows: 2, maxRows: 3}"
                placeholder="请输入内容"
                v-model="summary">
            </el-input>
        </div>
        <h3>编写内容</h3>
        <wangEditor ref="editor"/>
        <el-button type="primary" :loading="false" @click="publishPost()">发布<i class="el-icon-upload2"></i></el-button>
    </div>
</template>

<script>
import wangEditor from '@/components/WangEditor.vue'
import MulSelect from '@/components/MulSelect.vue'

export default {
    name:'editor',
    components:{
        wangEditor,
        MulSelect,
    },
    data() {
        return {
            title: '',
            categroy: '',
            label: '',
            summary:''
        }
    },

    methods:{
        getCategory(){
            this.$get(this.$API.API_GET_CATEGORY
            ).then(res => {
                if (res.code == 200){
                    this.categroy = res.data
                }else{
                    console.log(res.msg)
                }
            })
        },

        getLabel(){
            this.$get(this.$API.API_GET_LABEL
            ).then(res => {
                if (res.code == 200) {
                    this.label = res.data
                } else {
                    console.log(res.msg)
                }
            })
        },

        publishPost(){
            // 校验
            if (this.title.length==0) {
                this.$message({
                    message:'标题还有没输入',
                    type:'warning'
                })
                return
            }
            if (this.$refs.M1.selected.length==0) {
                this.$message({
                    message:'请选择分类',
                    type:'warning'
                })
                return
            }
            if (this.$refs.M2.selected.toString().length==0) {
                this.$message({
                    message:'请选择标签',
                    type:'warning'
                })
                return
            }
            if (this.$refs.editor.latestContent.length==0) {
                this.$message({
                    message:'内容还没有编写',
                    type:'warning'
                })
                return
            }
            if (this.summary.length==0) {
                this.$message({
                    message:'还需要编写摘要',
                    type:'warning'
                })
                return
            }

            this.$post(this.$API.API_PUT_POST,{
                title:this.title,
                summary:this.summary,
                categoryId:this.$refs.M1.selected,
                labelId:this.$refs.M2.selected.toString(),
                content:this.$refs.editor.latestContent,
                imgList:this.$refs.editor.getImgList(),
            }).then(res => {
                if (res.code == 200) {
                    this.title = '';
                    this.summary = '';
                    this.$refs.M1.selected = '';
                    this.$refs.M2.selected = '';
                    this.$refs.editor.clear();
                    this.$message({
                        showClose: true,
                        message: '发布成功',
                        type: 'success'
                    });
                } else {
                    this.$message({
                        showClose: true,
                        message: '发布失败',
                        type: 'error'
                    });
                }
            })
        }
    },

    mounted(){
        this.getCategory()
        this.getLabel()
        
    }
}
</script>

<style scoped>
    .content-title{
        margin: 25px 0 20px 0;
        font-weight: 300;
    }
    h3,h4{
        font-weight: 300;
        margin-bottom: 5px;
        margin-top: 25px;
    }
    .category-item div,.label-item div,.category-item,
    .label-item,.divide,.title-item span{
        display: inline-block;
    }
    .el-input,.el-textarea{
        width: 90%;
    }
    
    .divide{
        margin: 0 10px;
    }
    .title-item{
        width: 500px;
        margin: 10px 0 15px 0;
    }
    .post-desc{
        margin-bottom: 15px;
    }
    span{
        font-size: 12px;
        font-weight: 200;
        margin-right: 5px;
    }
    .post-content-span{
        font-size: 18px;
    }
    .el-button{
        float:right;
        padding: 10px;
        margin: 15px 0 30px 0;
    }
    .postp-content {
	animation: fade-in-bottom 0.6s ; ;
    }
    @keyframes fade-in-bottom {
        0% {
            transform: translateY(50px);
            opacity: 0;
        }
        100% {
            transform: translateY(0);
            opacity: 1;
        }
    }
</style>
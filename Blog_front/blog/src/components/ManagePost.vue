<template>
    <div class="epost-content">
        <h2 class="content-title">管理博客</h2>
        <div>
            <el-table
              :data="posts"
              border
              style="width: 100%"
              height="400"
            >
                <el-table-column
                  fixed
                  prop="id"
                  label="ID"
                  width="50"
                >
                </el-table-column>
                <el-table-column
                  prop="title"
                  label="标题"
                  width="200"
                >
                </el-table-column>
                <el-table-column
                  prop="author"
                  label="作者"
                  width="70"
                >
                </el-table-column>
                <el-table-column
                  label="简要"
                  width="240"
                >
                    <template slot-scope="scope">
                        <el-tooltip :content="scope.row.summary">
                            <div class="post-summary" title="显示全部">
                                {{scope.row.summary}}
                            </div>
                        </el-tooltip>
                    </template>
                </el-table-column>
                <el-table-column
                  prop="publishTime"
                  label="时间"
                  width="150"
                >
                </el-table-column>
                <el-table-column
                  width="240"
                  label="内容"
                  max-height="200"
                >
                    <template slot-scope="scope">
                        <el-tooltip :content="markdownIt.render(scope.row.content)">
                            <div class="post-md" title="显示全部">
                                {{markdownIt.render(scope.row.content)}}
                            </div>
                        </el-tooltip>
                    </template>
                </el-table-column>
                <el-table-column
                  label="分类"
                  prop="categoryName"
                >

                </el-table-column>
                <el-table-column
                  label="标签"
                  width="100"
                >
                    <template slot-scope="scope">
                        <div class="label-item">
                            <span v-for="(item,index) in scope.row.labelName" :key="index" class="label">
                                {{item}}
                            </span>
                        </div>
                    </template>
                </el-table-column>
                <el-table-column
                  fixed="right"
                  label="操作"
                  width="120"
                >
                <template slot-scope="scope">
                    <el-button @click="view(scope.row)" type="text" size="small">查看</el-button>
                    <el-button @click="edit(scope.row)" type="text" size="small">编辑</el-button>
                    <el-button @click="del(scope.row.id)" type="text" size="small">删除</el-button>
                </template>
                </el-table-column>
                <el-table-column
                  prop="read_counts"
                  label="阅读数"
                  width="70"
                >
                </el-table-column>
                <el-table-column
                  prop="comment_counts"
                  label="评论数"
                  width="70"
                >
                </el-table-column>
                <el-table-column
                  prop="like_counts"
                  label="点赞数"
                  width="70"
                >
                </el-table-column>
            </el-table>
        </div>
        <el-dialog
         title="查看"
         :visible.sync="viewPost"
         width="70%"
         top="5vh"
         center
        >
            <h2 class="current-post-title">{{this.currentPost.title}}</h2>
            <div class="desc">
                <div class="author">
                    作者：{{this.currentPost.author}}
                </div>
                <div class="time">
                    发布时间：{{this.currentPost.publishTime}}
                </div>
                <div class="category">
                    分类：{{this.currentPost.categoryName}}
                </div>
                <div class="label">
                    <span>
                        标签：
                    </span>
                    <span v-for="(item,index) in this.currentPost.labelName" :key="index">
                        {{item}}
                    </span>
                </div>
                <div class="summary">
                    <div>
                        简要：
                    </div>
                    <div>
                        {{this.currentPost.summary}}
                    </div>
                </div>
            </div>
            <mavon-editor
              :value="this.currentPost.content"
              :subfield="false"
              :defaultOpen="'preview'"
              :toolbarsFlag="false"
              :shortCut='false'
              :editable="false"
              :ishljs="true"
            />
            <div class="count">
                <span>点赞({{this.currentPost.like_counts}})</span>
                <span class="read-item">阅读({{this.currentPost.read_counts}})</span>
                <span>评论({{this.currentPost.comment_counts}})</span>
            </div>
            <div style="clear:both;"></div>
        </el-dialog>
        <el-dialog
          title="编辑"
          :visible.sync="editPost"
          width="70%"
          top="5vh"
          center
        >
            <mavon-editor 
              v-model="currentPost.content"
              :toolbars="toolbars"
              :subfield=false
              defaultOpen='edit'
              @imgAdd="ImgUpload"
              @imgDel="ImgDel"
              ref='md'
            />
        </el-dialog>
    </div>
</template>

<script>
import { mavonEditor } from 'mavon-editor'
import axios from 'axios';

export default {
    name:'editor',
    data() {
        return {
            posts:[],
            markdownIt:mavonEditor.getMarkdownIt(),
            viewPost:false,
            editPost:false,
            currentPost:'',
            toolbars: {
                bold: true, // 粗体
                italic: true, // 斜体
                header: true, // 标题
                underline: true, // 下划线
                strikethrough: true, // 中划线
                mark: true, // 标记
                superscript: true, // 上角标
                subscript: true, // 下角标
                quote: true, // 引用
                ol: true, // 有序列表
                ul: true, // 无序列表
                link: true, // 链接
                imagelink: true, // 图片链接
                code: true, // code
                table: true, // 表格
                fullscreen: true, // 全屏编辑
                readmodel: true, // 沉浸式阅读
                htmlcode: true, // 展示html源码
                help: true, // 帮助
                /* 1.3.5 */
                undo: true, // 上一步
                redo: true, // 下一步
                trash: true, // 清空
                save: false, // 保存（触发events中的save事件）
                /* 1.4.2 */
                navigation: true, // 导航目录
                /* 2.1.8 */
                alignleft: true, // 左对齐
                aligncenter: true, // 居中
                alignright: true, // 右对齐
                /* 2.2.1 */
                subfield: true, // 单双栏模式
                preview: true, // 预览
            }
        }
    },

    mounted(){
        this.getPosts()
    },
    methods:{
        getPosts(){
            this.$get(this.$API.API_GET_POSTS,{
                "total":"True"
            }).then(res => {
                if (res.code == 200) {
                    this.posts = res.data;
                }
            })
        },
        view(content){
            this.viewPost = true;
            this.currentPost = content
        },
        getBase64Image(img) {
            const canvas = document.createElement('canvas')
            canvas.width = img.width
            canvas.height = img.height
            const ctx = canvas.getContext('2d')
            ctx.drawImage(img, 0, 0, canvas.width, canvas.height)
            const dataURL = canvas.toDataURL()
            return dataURL
        },
        edit(content){
            this.editPost = true;
            this.currentPost = content;
            this.$nextTick(function () {
                console.log(this.$refs.md.$refs.toolbar_left.img_file);
                // let img = new Image();
                // let canvas=document.createElement("canvas"),//获取canvas
                // ctx = canvas.getContext("2d")
                // img.crossOrigin = "anonymous"
                // img.src = "http://localhost:8000/static/upload/blog/2022042417273927263.jpg"
                // img.onload = function(){
                //     ctx.drawImage(img,0,0);
                //     console.log(canvas.toDataURL("image/jepg"))
                // }

                
                // let _file = new File([],"白易子教主 高叉毛衣_6.jpg",{
                //     "type":"image/jpeg",
                // })
                // this.$refs.md.$refs.toolbar_left.img_file.push({
                //     "0":"http://localhost:8000/static/upload/blog/2022042720392475070.jpg",
                //     "1":_file
                // })
            })
        },
        del(row){
            console.log(row)
        },
        ImgDel(pos){
            let img = pos[0];
            this.$del(this.$API.API_UPLOAD_IMG,{
                "img":img
            }).then(res => {
                console.log(res.msg);
            })
        },
        ImgUpload(pos,$file){
            var formdata = new FormData();
            formdata.append("img", $file);
            
            axios.post(
                this.$API.API_UPLOAD_IMG,
                formdata,
                {
                    headers:{'Content-Type':'multipart/form-data'}
                }
            ).then(res => {
                this.$refs.md.$img2Url(pos, this.$API.BASE_SERVER_URL+res.data.url);
            })
        },
    },
}
</script>

<style scoped lang='less'>
    .content-title{
        margin: 25px 0 20px 0;
        font-weight: 300;
    }
    .post-md,.post-summary{
        -webkit-box-orient: vertical;
        text-overflow: ellipsis;
        display: -webkit-box;
		-webkit-line-clamp: 3;
        overflow: hidden;
    }
    .label{
        display: block;
    }
    .current-post-title{
        color: black;
        margin-bottom: 10px;
    }
    .desc{
        margin-bottom: 10px;
        background: #f8f8f8;
        border-radius: 4px;
        padding: 5px 10px;
        font-size: 14px;
        font-weight: 200;
    }
    .summary{
        display: flex;
    }
    .count{
        float: right;
        margin-top: 5px;
        font-size: 12px;
        font-weight: 200;
        span{
            margin-left: 3px;
        }
    }
</style>
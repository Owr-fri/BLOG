<template>
  <div class="epost-content">
    <h2 class="content-title">管理博客</h2>
    <div>
      <el-table :data="posts" border style="width: 100%" height="calc(70vh)" size="mini" v-loading="tabelLoading" element-loading-text="拼命加载中" element-loading-spinner="el-icon-loading">
        <el-table-column fixed prop="id" label="ID" width="60" sortable>
        </el-table-column>
        <el-table-column prop="title" label="标题" width="200">
        </el-table-column>
        <el-table-column prop="author" label="作者" width="70">
        </el-table-column>
        <el-table-column label="简要" width="240">
          <template slot-scope="scope">
            <el-tooltip :content="scope.row.summary">
              <div class="post-summary" title="显示全部">
                {{scope.row.summary}}
              </div>
            </el-tooltip>
          </template>
        </el-table-column>
        <el-table-column prop="publishTime" label="时间" width="150">
        </el-table-column>
        <el-table-column width="240" label="内容" max-height="200">
          <template slot-scope="scope">
            <el-tooltip :content="markdownIt.render(scope.row.content)">
              <div class="post-md" title="显示全部">
                {{markdownIt.render(scope.row.content)}}
              </div>
            </el-tooltip>
          </template>
        </el-table-column>
        <el-table-column label="分类" prop="categoryName">

        </el-table-column>
        <el-table-column label="标签" width="100">
          <template slot-scope="scope">
            <div class="label-item">
              <span v-for="(item,index) in scope.row.labelName" :key="index" class="label">
                {{item}}
              </span>
            </div>
          </template>
        </el-table-column>
        <el-table-column fixed="right" label="操作" width="120">
          <template slot-scope="scope">
            <el-button @click="view(scope.row)" type="text" size="mini">查看</el-button>
            <el-button @click="edit(scope.row)" type="text" size="mini">编辑</el-button>
            <el-button @click="del(scope.row)" type="text" size="mini">删除</el-button>
          </template>
        </el-table-column>
        <el-table-column prop="read_counts" label="阅读数" width="85" sortable>
        </el-table-column>
        <el-table-column prop="comment_counts" label="评论数" width="85" sortable>
        </el-table-column>
        <el-table-column prop="like_counts" label="点赞数" width="85" sortable>
        </el-table-column>
      </el-table>
    </div>
    <el-dialog title="查看" :visible.sync="viewPost" width="70%" top="5vh" center>
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
      <mavon-editor :value="this.currentPost.content" :subfield="false" :defaultOpen="'preview'" :toolbarsFlag="false" :shortCut='false' :editable="false" :ishljs="true" />
      <div class="count">
        <span>点赞({{this.currentPost.like_counts}})</span>
        <span class="read-item">阅读({{this.currentPost.read_counts}})</span>
        <span>评论({{this.currentPost.comment_counts}})</span>
      </div>
      <div style="clear:both;"></div>
    </el-dialog>
    <el-dialog title="编辑" :visible.sync="editPost" :close-on-click-modal="false" width="70%" top="5vh">
      <el-form ref="form" :model="currentPost" :label-position="'left'" label-width="40px" size="mini">
        <el-form-item label="标题">
          <el-input type="text" placeholder="请输入内容" v-model="currentPost.title" maxlength="50" show-word-limit size='small'>
          </el-input>
        </el-form-item>
        <el-form-item label="分类">
          <el-select v-model="currentPost.categoryId" filterable allow-create :multiple="false" placeholder="请选择" size='mini'>
            <el-option v-for="item in category" :key="item.id" :label="item.name" :value="item.id">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="标签">
          <el-select v-model="currentPost.labelId" filterable allow-create :multiple="true" placeholder="请选择" size='mini'>
            <el-option v-for="item in label" :key="item.id" :label="item.name" :value="item.id">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="简要">
          <el-input type="textarea" maxlength=100 show-word-limit :autosize="{ minRows: 2, maxRows: 3}" placeholder="请输入内容" v-model="currentPost.summary">
          </el-input>
        </el-form-item>
        <mavon-editor v-model="currentPost.content" :toolbars="toolbars" :subfield=false defaultOpen='edit' @imgAdd="ImgUpload" @imgDel="ImgDel" ref='md' />
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button type="danger" @click="editPost = false" plain size="small">取 消</el-button>
        <el-button type="primary" @click="updatePost" plain size="small" :loading="loading">保 存</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
  import { mavonEditor } from 'mavon-editor'
  import axios from 'axios';

  export default {
    name: 'editor',
    data() {
      return {
        posts: [],
        markdownIt: mavonEditor.getMarkdownIt(),
        viewPost: false,
        editPost: false,
        label: '',
        category: '',
        currentPost: '',
        delImgList: [],
        tabelLoading: true,
        loading: false,
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


    mounted() {
      this.getPosts()
      this.getLabel()
      this.getCategory()
    },
    methods: {
      getCategory() {
        this.$get(this.$API.API_GET_CATEGORY).then(res => {
          if (res.code == 200) {
            this.category = res.data
          } else {
            console.log(res.msg)
          }
        })
      },
      getLabel() {
        this.$get(this.$API.API_GET_LABEL).then(res => {
          if (res.code == 200) {
            this.label = res.data
          } else {
            console.log(res.msg)
          }
        })
      },
      getPosts() {
        this.$get(this.$API.API_GET_POSTS, {
          "status": "1"
        }).then(res => {
          if (res.code == 200) {
            this.posts = res.data;
            this.tabelLoading = false;
          }
        })
      },
      view(content) {
        this.viewPost = true;
        this.currentPost = content
      },
      blobToBase64(blob) {
        return new Promise((resolve, reject) => {
          const fileReader = new FileReader();
          fileReader.onload = (e) => {
            resolve(e.target.result);
          };
          fileReader.readAsDataURL(blob);
          fileReader.onerror = () => {
            reject(new Error('blobToBase64 error'));
          };
        });
      },
      edit(content) {
        this.editPost = true;
        this.currentPost = content;
        this.$nextTick(function () {
          let _content = this.currentPost.content

          // 从文章内容提取图片链接，添加到缩略图列表中
          let reg = /(!.*?[)][\n]?)/g
          if (_content.match(reg)) {
            _content.match(reg).forEach(i => {
              let imgName = i.split(']')[0].substring(2, ).split('.')[0]
              let link = i.split(']')[1].substring(1, i.split(']')[1].length - 1)
              let linkparam = link.split("static")[1]

              axios.get(this.$API.API_GET_IMG, {
                params: {
                  "img": linkparam
                },
                responseType: 'blob'
              }).then(res => {
                this.blobToBase64(res).then(result => {
                  let _file = new File([result], imgName, { "type": "image/jpeg" })
                  _file.miniurl = result;
                  _file._name = imgName;
                  this.$refs.md.$refs.toolbar_left.img_file.push({
                    '0': link,
                    "1": _file,
                  })
                })
              })
            });
          }
        })
      },
      del(row) {
        this.$del(this.$API.API_PUT_POST, {
          'id': row.id
        }).then(res => {
          if (res.code == 200) {
            this.$message({
              message: res.msg,
              type: 'success'
            })
          }
          this.posts = this.posts.filter((i) => {
            return i.id != row.id
          })
        })
      },
      ImgDel(pos) {
        let img = pos[0];
        // 获取所有的图片链接，找出删除的链接，在文中删除
        let reg = /(!.*?[)][\n]?)/g
        let imglist = this.currentPost.content.match(reg)
        if (imglist) {
          imglist.forEach(i => {
            let link = i.match(/[(](.*?)[)]/g)[0]
            link = link.substring(1, link.length - 1)
            if (link === img) {
              const items = this.currentPost.content.split(i)
              this.currentPost.content = items.join('')
            }
          });
        }
        this.delImgList.push(img)
        this.$message({
          message: '删除成功',
          type: 'success'
        })
      },
      ImgUpload(pos, $file) {
        var formdata = new FormData();
        formdata.append("img", $file);

        axios.post(
          this.$API.API_UPLOAD_IMG,
          formdata,
          {
            headers: { 'Content-Type': 'multipart/form-data' }
          }
        ).then(res => {
          this.$refs.md.$img2Url(pos, this.$API.BASE_SERVER_URL + res.data.url);
        })
      },
      updatePost() {
        this.loading = true;
        // 删除图片
        if (this.delImgList) {
          this.delImgList.forEach(i => {
            this.$del(this.$API.API_UPLOAD_IMG, {
              "img": i
            }).then(res => {
              if (res.code == 200) {
                console.log(res.msg);
              }
            })
          });
        }


        // 修改内容
        let formData = new FormData()
        formData.append('id', this.currentPost.id);
        formData.append('title', this.currentPost.title);
        formData.append('label', this.currentPost.labelId.toString());
        formData.append('category', this.currentPost.categoryId);
        formData.append('summary', this.currentPost.summary);
        formData.append('content', this.currentPost.content);

        this.$put(this.$API.API_PUT_POST, formData).then(res => {
          if (res.code == 200) {
            this.$message({
              message: '保存成功',
              type: 'success'
            })
            this.$refs.md.$refs.toolbar_left.img_file = []
            this.loading = false;
            this.editPost = false;
          } else {
            this.$message({
              message: '保存失败',
              type: 'error'
            })
          }
        })
      }
    },
  }
</script>

<style scoped lang='less'>
  .content-title {
    margin: 25px 0 20px 0;
    font-weight: 300;
  }

  .post-md,
  .post-summary {
    -webkit-box-orient: vertical;
    text-overflow: ellipsis;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    overflow: hidden;
  }

  .label {
    display: block;
  }

  .current-post-title {
    color: black;
    margin-bottom: 10px;
  }

  .desc {
    margin-bottom: 10px;
    background: #f8f8f8;
    border-radius: 4px;
    padding: 5px 10px;
    font-size: 14px;
    font-weight: 200;
  }

  .summary {
    display: flex;
  }

  .count {
    float: right;
    margin-top: 5px;
    font-size: 12px;
    font-weight: 200;

    span {
      margin-left: 3px;
    }
  }
</style>
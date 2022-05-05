<template>
  <div class="postp-content">
    <h2 class="content-title">发布博客</h2>
    <div class="title-item">
      <span>标题</span>
      <el-input type="text" placeholder="请输入内容" v-model="title" maxlength="50" show-word-limit size='small'>
      </el-input>
    </div>
    <div class="post-desc">
      <div class="category-item">
        <span>分类</span>
        <el-select v-model="categroySelected" filterable allow-create :multiple="false" placeholder="请选择" size='mini'>
          <el-option v-for="item in categroy" :key="item.id" :label="item.name" :value="item.id">
          </el-option>
        </el-select>
      </div>
      <div class="divide"> </div>
      <div class="label-item">
        <span>标签</span>
        <el-select v-model="labelSelected" filterable allow-create :multiple="true" placeholder="请选择" size='mini'>
          <el-option v-for="item in label" :key="item.id" :label="item.name" :value="item.id">
          </el-option>
        </el-select>
      </div>
    </div>
    <div class="post-summary">
      <h4>摘要</h4>
      <el-input type="textarea" maxlength=100 show-word-limit :autosize="{ minRows: 2, maxRows: 3}" placeholder="请输入内容" v-model="summary">
      </el-input>
    </div>
    <h3>编写内容</h3>
    <mavon-editor v-model="content" :toolbars="toolbars" :subfield=false defaultOpen='edit' @imgAdd="ImgUpload" @imgDel="ImgDel" ref='md' v-if="show" />
    <el-button type="primary" :loading="false" @click="publishPost()">发布<i class="el-icon-upload2"></i></el-button>
  </div>
</template>

<script>
  import axios from 'axios';

  export default {
    name: 'editor',
    data() {
      return {
        title: '',
        categroy: '',
        categroySelected: '',
        label: '',
        labelSelected: [],
        summary: '',
        show: true,
        content: '',
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

    mounted() {
      this.getCategory()
      this.getLabel()

      // const markdownIt = this.$refs.md
      // console.log(markdownIt.getMarkdownIt());
    },

    methods: {
      getCategory() {
        this.$get(this.$API.API_GET_CATEGORY).then(res => {
          if (res.code == 200) {
            this.categroy = res.data
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
      ImgDel(pos) {
        let img = pos[0];
        this.$del(this.$API.API_UPLOAD_IMG, {
          "img": img
        }).then(res => {
          console.log(res.msg);
        })
      },

      publishPost() {
        // 校验
        console.log(this.$refs.md.$refs.toolbar_left.img_file);
        if (this.title.length == 0) {
          this.$message({
            message: '标题还有没输入',
            type: 'warning'
          })
          return
        }
        if (this.labelSelected.length == 0) {
          this.$message({
            message: '请选择分类',
            type: 'warning'
          })
          return
        }
        if (this.categroySelected.toString().length == 0) {
          this.$message({
            message: '请选择标签',
            type: 'warning'
          })
          return
        }
        if (this.content.length == 0) {
          this.$message({
            message: '内容还没有编写',
            type: 'warning'
          })
          return
        }
        if (this.summary.length == 0) {
          this.$message({
            message: '还需要编写摘要',
            type: 'warning'
          })
          return
        }

        this.$post(this.$API.API_PUT_POST, {
          title: this.title,
          summary: this.summary,
          categoryId: this.categroySelected,
          labelId: this.labelSelected.toString(),
          content: this.content,
        }).then(res => {
          if (res.code == 200) {
            this.$message({
              showClose: true,
              message: '发布成功',
              type: 'success'
            });
            // location.reload()
            this.title = '';
            this.categroySelected = '';
            this.labelSelected = '';
            this.summary = '';
            this.content = '';
            this.$refs.md.$refs.toolbar_left.img_file = []
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
  }
</script>

<style scoped>
  .content-title {
    margin: 25px 0 20px 0;
    font-weight: 300;
  }

  h3,
  h4 {
    font-weight: 300;
    margin-bottom: 5px;
    margin-top: 25px;
  }

  .category-item div,
  .label-item div,
  .category-item,
  .label-item,
  .divide,
  .title-item span {
    display: inline-block;
  }

  .el-input,
  .el-textarea {
    width: 90%;
  }

  .divide {
    margin: 0 17px;
  }

  .title-item {
    width: 500px;
    margin: 10px 0 15px 0;
  }

  .post-desc {
    margin-bottom: 15px;
  }

  span {
    font-size: 12px;
    font-weight: 200;
    margin-right: 5px;
  }

  .post-content-span {
    font-size: 18px;
  }

  .el-button {
    float: right;
    padding: 10px;
    margin: 15px 0 30px 0;
  }

  .postp-content {
    animation: fade-in-bottom 0.6s;
    ;
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
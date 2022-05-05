<template>
  <div>
    <el-page-header @back="goBack" :content="pictureTitle">
    </el-page-header>
    <h2 class="title">图片</h2>
    <vuedraggable tag="ul" draggable=".draggable-item" class="drag-div" v-bind="dragOptions" v-model="imgList">
      <!-- 拖拽元素 -->
      <li v-for="(item) in imgList" :key="item.id" class="draggable-item">
        <el-image :src="$API.BASE_SERVER_URL+item.img" :preview-src-list="[$API.BASE_SERVER_URL+item.img]" :style="{width:'140px',height:'140px'}" :fit="'cover'"></el-image>
        <div class="shadow" @click="onRemoveHandler(item.id)">
          <i class="el-icon-delete"></i>
        </div>
      </li>
      <el-upload action="#" :multiple="true" :limit=20 :show-file-list="false" accept=".jpg,.jpeg,.png,.gif.JPG,.JPEG,.PNG,.GIF" class="avatar-uploader" :http-request="imgUpload" :on-exceed="handleLimit">
        <i slot="default" class="el-icon-plus avatar-uploader-icon"></i>
      </el-upload>
    </vuedraggable>
    <div class="divide"></div>
    <h2 class="summary">简要</h2>
    <div style="width:100%;display:inline-block;">
      <el-input type="textarea" autosize placeholder="请输入内容" maxlength="150" show-word-limit v-model="summary">
      </el-input>
      <el-button type="primary" :loading="isload" @click="submitUpload">发布<i class="el-icon-upload2"></i></el-button>
    </div>
  </div>
</template>
<script>
  import vuedraggable from 'vuedraggable'

  export default {
    data() {
      return {
        name: this.$route.params["name"],
        imgList: [],
        summary: '',
        isload: false,
        imageUrl: '',
        dragOptions: { animation: 500 },
      };
    },
    computed: {
      pictureTitle() {
        return /\d*年\d*月\d*日/.exec(this.name)[0]
      }
    },
    components: {
      vuedraggable
    },
    mounted() {
      this.getPictureDesc()
    },
    methods: {
      getPictureDesc() {
        let title = this.name;
        this.$get(this.$API.API_GET_PICTURE_DESC, {
          'title': title
        }).then(res => {
          this.imgList = res.data.imglist;
          this.summary = res.data.summary;
        })
      },
      goBack() {
        this.$router.push("/manage/mpicture")
      },
      imgUpload(params) {
        let file = params.file;
        let isLt50M = file.size / 1024 / 1024 < 50;
        if (!isLt50M) {
          this.$message({
            message: '图片大小超出50M',
            type: 'success',
          })
        }
        let formdata = new FormData();
        formdata.append("file", file);
        formdata.append("title", this.name);
        formdata.append("summary", this.summary);
        this.$put(this.$API.API_UPDATE_PICUTRE, formdata).then(res => {
          if (res.code == 200) {
            this.imgList.push(res.data)
          }
        })
      },
      onRemoveHandler(id) {
        this.$del(this.$API.API_UPDATE_PICUTRE, {
          "id": id
        }).then(res => {
          if (res.code == 200) {
            this.$message({
              message: res.msg,
              type: 'success',
            })
            this.imgList = this.imgList.filter(i => {
              return i.id != id
            })
          }
        })
      },
      submitUpload() {
        if (this.imgList.length == 0) {
          this.$message({
            message: '请选择上传的图片',
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

        let fromdata = new FormData()
        let imglist = []
        this.imgList.forEach(element => {
          imglist.push(element.id)
        });
        fromdata.append("imglist", imglist)
        fromdata.append("summary", this.summary)
        this.$put(this.$API.API_UPLOAD_PICTURE, fromdata).then(res => {
          this.$message({
            message: res.msg,
            type: 'success'
          })
        })
      },
      handleLimit() {
        this.$message({
          message: "一次最多上传20张图片",
          type: 'warning',
        })
      },
    },
  };
</script>
<style lang="less" scoped>
  .title,
  .summary {
    margin: 5px 0 5px 0;
    font-weight: 300;
  }

  li {

    vertical-align: middle;
    list-style: none;
    margin-right: 5px;
    margin-bottom: 5px;
    border: 1px solid #ddd;
    border-radius: 6px;
    position: relative;
    overflow: hidden;
  }

  .drag-div {
    flex-wrap: wrap;
    display: flex;
  }

  .avatar-uploader .el-upload {
    border: 1px dashed #d9d9d9;
    border-radius: 6px;
    cursor: pointer;
    position: relative;
    overflow: hidden;
  }

  .avatar-uploader .el-upload:hover {
    border-color: #409EFF;
  }

  .avatar-uploader-icon {
    font-size: 28px;
    color: #8c939d;
    width: 140px;
    height: 140px;
    line-height: 140px;
    text-align: center;
  }

  .avatar {
    width: 140px;
    height: 140px;
    display: block;
  }

  .avatar-uploader {
    background-color: #fbfdff;
    border: 1px dashed #c0ccda;
    border-radius: 6px;
    width: 142px;
    height: 146px;
    box-sizing: border-box;
    vertical-align: top;
  }

  .avatar-uploader:hover {
    border: 1px dashed #409EFF;
  }

  .shadow {
    position: absolute;
    top: 0;
    right: 0;
    background-color: rgba(0, 0, 0, .5);
    opacity: 0;
    transition: all .3s;
    color: #fff;
    font-size: 20px;
    line-height: 20px;
    padding: 2px;
    cursor: pointer;
  }

  .draggable-item:hover {
    .shadow {
      opacity: 1;
    }
  }

  .el-button {
    float: right;
    padding: 10px;
    margin: 10px 0 30px 0;
  }

  .divide {
    width: 60%;
    margin: 20px auto 10px auto;
    border-top: 1px solid #e8ecf1;
  }
</style>
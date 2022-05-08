<template>
  <div class="p-picture">
    <h2 class="content-title">发布图集</h2>
    <div>
      <div class="picture">
        <span class="picture-head">图片集</span>
        <div style="width:90%;display:inline-block;vertical-align: top;">
          <el-upload action='' ref="upload" list-type="picture-card" :multiple='true' :auto-upload="false" :on-preview="handlePictureCardPreview" :on-remove="handleRemove" :on-change="handleFileChange" :before-remove="handleFileRemove" :file-list="imgList" :limit=20 accept=".jpg,.jpeg,.png,.gif.JPG,.JPEG,.PNG,.GIF" :on-exceed="handleLimit">
            <i slot="default" class="el-icon-plus"></i>
            <div slot="file" slot-scope="{file}">
              <img class="el-upload-list__item-thumbnail" :src="file.url" alt="">
              <span class="el-upload-list__item-actions">
                <span class="el-upload-list__item-preview" @click="handlePictureCardPreview(file)">
                  <i class="el-icon-zoom-in"></i>
                </span>
                <span v-if="!disabled" class="el-upload-list__item-delete" @click="handleRemove(file)">
                  <i class="el-icon-delete"></i>
                </span>
              </span>
            </div>
          </el-upload>
          <el-dialog :visible.sync="dialogVisible">
            <img width="100%" :src="dialogImageUrl" alt="">
          </el-dialog>
        </div>
      </div>
      <span class="summary">介绍</span>
      <div style="width:90%;display:inline-block;">
        <el-input type="textarea" autosize placeholder="请输入内容" maxlength="150" show-word-limit v-model="summary">
        </el-input>
        <el-button type="primary" :loading="isload" @click="submitUpload">发布<i class="el-icon-upload2"></i></el-button>
      </div>
    </div>

  </div>
</template>

<script>
  import axios from 'axios';

  export default {
    data() {
      return {
        dialogImageUrl: '',
        dialogVisible: false,
        disabled: false,
        summary: '',
        imgList: [],
        isload: false,
      };
    },
    methods: {
      handleRemove(file) {
        let uploadFiles = this.$refs.upload.uploadFiles
        for (var i = 0; i < uploadFiles.length; i++) {
          if (uploadFiles[i]['url'] == file.url) {
            uploadFiles.splice(i, 1)
          }
        }
      },
      handlePictureCardPreview(file) {
        this.dialogImageUrl = file.url;
        this.dialogVisible = true;
      },

      submitUpload() {
        let types = ['image/jpeg', 'image/jpg', 'image/gif', 'image/bmp', 'image/png'];

        if (this.imgList.length == 0) {
          this.$message({
            message: '请选择上传的图片',
            type: 'warning'
          })
          return
        }

        for (let index = 0; index < this.imgList.length; index++) {
          let intypes = types.includes(this.imgList[index].raw.type)
          if (!intypes) {
            this.$message({
              message: '图片格式错误',
              type: 'warning'
            })
            return
          }
        }

        if (this.summary.length == 0) {
          this.$message({
            message: '还需要编写摘要',
            type: 'warning'
          })
          return
        }

        let fd = new FormData()
        this.imgList.forEach(file => {
          fd.append('file', file.raw);
        });
        fd.append('summary', this.summary)

        this.isload = true;
        axios.post(
          this.$API.API_PICTURE,
          fd,
          {
            headers: { 'Content-Type': 'multipart/form-data' }
          }
        ).then(res => {
          this.isload = false
          if (res.code == 200) {
            this.imgList = []
            this.summary = ''
            this.$message({
              message: res.msg,
              type: 'success',
            })
          }
        }).catch(error => {
          console.log(error)
        })
      },

      // 上传发生变化钩子
      handleFileChange(file, fileList) {
        this.imgList = fileList;
      },
      // 删除之前钩子
      handleFileRemove(file, fileList) {
        this.imgList = fileList;
      },
      handleLimit(file, fileList) {
        this.imgList = fileList
        this.$message({
          message: "一次最多上传20张图片",
          type: 'warning',
        })
      }
    }
  }
</script>

<style lang="less" scoped>
  .content-title {
    margin: 25px 0 25px 0;
    font-weight: 300;
  }

  .summary,
  .picture-head {
    font-size: 14px;
    font-weight: 200;
    vertical-align: top;
    margin-right: 10px;
  }

  .summary {
    margin-right: 22px;
  }

  .picture {
    margin-bottom: 20px;
  }

  .el-button {
    float: right;
    padding: 10px;
    margin: 10px 0 30px 0;
  }

  /deep/ .el-dialog {
    max-width: 70%;
    width: auto;
  }

  .p-picture {
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
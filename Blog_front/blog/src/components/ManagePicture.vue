<template>
  <div class="manage-picture">
    <h2 class="content-title">管理图集</h2>
    <div class="isloading" v-if="isloading">
      <loading />
    </div>
    <div>
      <el-row :gutter="20" v-for="(i,index) in row" :key="index" :style="{ marginTop:'10px' }">
        <el-col :span="8" v-for="(j,index) in 3" :key="index">
          <el-card :body-style="{ padding: '0px' }" v-if="pictures[(i-1)*3+j-1]" shadow="hover" class="card">
            <el-image :src="$API.BASE_SERVER_URL+pictures[(i-1)*3+j-1].img" class="image" :fit='"cover"' :alt="pictures[(i-1)*3+j-1].title"></el-image>
            <div style="padding: 6px;">
              <time>{{ /\d*年\d*月\d*日/.exec(pictures[(i-1)*3+j-1].title)[0] }}</time>
                <div class="desc">"{{pictures[(i-1)*3+j-1].summary}}"</div>
                <div class="bottom clearfix">
                  <el-button type="primary" class="button" size="mini" @click="edit(pictures[(i-1)*3+j-1].title)">编辑</el-button>
                  <el-button type="info" class="button" size="mini" @click="getPictureDesc(pictures[(i-1)*3+j-1].title)">展示</el-button>
                  <el-button type="danger" class="button" size="mini" @click="del(pictures[(i-1)*3+j-1].title)">删除</el-button>
                </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>
    <el-dialog :title="currentTitle" width="70%" center :visible.sync="dialogShow" :before-close="cleanImgList">
      <el-image :src="item" :fit='"fit"' v-for="item in currentImgList" :key="item.id" lazy :preview-src-list="currentImgList"></el-image>
    </el-dialog>
  </div>
</template>

<script>
  import loading from "./loading.vue"

  export default {
    name: 'manage-picture',
    data() {
      return {
        loading: false,
        isloading: true,
        dialogShow: false,
        pictures: [],
        currentImgList: [],
        currentTitle: '',
      }
    },
    components: {
      loading
    },
    mounted() {
      this.getPictures()
    },
    computed: {
      row() {
        return Math.ceil(this.pictures.length / 3)
      }
    },
    methods: {
      getPictures() {
        this.$get(this.$API.API_PICTURE).then(res => {
          if (res.code == 200) {
            this.pictures = res.data;
            this.isloading = false;
          }
        })
      },
      getPictureDesc(title) {
        this.$get(this.$API.API_GET_PICTURE_DESC, {
          'title': title
        }).then(res => {
          this.dialogShow = true;
          this.currentTitle = /\d*年\d*月\d*日/.exec(res.data.title)[0];
          res.data.imglist.forEach(i => {
            this.currentImgList.push(this.$API.BASE_SERVER_URL + i.img)
          });

        })
      },
      cleanImgList(done) {
        done();
        this.currentImgList = [];
      },
      del(title) {
        this.$confirm('此操作将永久删除"' + title + '"图集, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          this.$del(this.$API.API_PICTURE, {
            'title': title
          }).then(res => {
            if (res.code == 200) {
              this.pictures = this.pictures.filter(i => {
                return i.title != title
              })
              this.$message({
                type: 'success',
                message: '删除成功!'
              });
            } else {
              this.$message({
                type: 'error',
                message: '删除失败!'
              });
            }
          })
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消删除'
          });
        });
      },
      edit(title) {
        this.$router.push({
          name: "ReEditPicture",
          params: {
            name: title,
          }
        })
      },
      beforeEnter(dom) {
        let { x = 0, y = 0, s = 1, opacity = 0 } = dom.dataset;
        dom.style.cssText = `transition: .3s;opacity: ${opacity};transform: scale(${s}) translateX(${x}) translateY(${y});`;
      },
      enter(dom, done) {
        let delay = dom.dataset.delay;
        setTimeout(function () {
          dom.style.cssText = `transition: .3s;opacity: 1;transform: scale(1) translateX(0) translateY(0);`;
          //监听 transitionend 事件
          var transitionend = window.ontransitionend ? "transitionend" : "webkitTransitionEnd";
          dom.addEventListener(transitionend, function onEnd() {
            dom.removeEventListener(transitionend, onEnd);
            done(); //调用done() 告诉vue动画已完成，以触发 afterEnter 钩子
          });
        }, delay)
      },
      afterEnter(dom) {
        dom.style.cssText = "";
      }
    },
  }
</script>

<style lang="less" scoped>
  .content-title {
    margin: 25px 0 5px 0;
    font-weight: 300;
  }

  .desc {
    font-size: 13px;
    color: #999;
  }

  .bottom {
    margin-top: 7px;
  }

  .button {
    margin-left: 3px !important;
    padding: 4px;
    float: right;
  }

  .image {
    width: 100%;
    height: 250px;
    display: block;
  }

  .clearfix:before,
  .clearfix:after {
    display: table;
    content: "";
  }

  .clearfix:after {
    clear: both
  }

  .manage-picture {
    margin-bottom: 20px;
  }

  /deep/ .el-dialog__body {
    text-align: center !important;
  }

  .isloading {
    margin-top: 150px;
    min-height: 50vh
  }

  .card {
    -webkit-animation: fade-in 1.4s;
    animation: fade-in 1.4s;
  }

  @-webkit-keyframes fade-in {
    0% {
      opacity: 0;
    }

    100% {
      opacity: 1;
    }
  }

  @keyframes fade-in {
    0% {
      opacity: 0;
    }

    100% {
      opacity: 1;
    }
  }
</style>
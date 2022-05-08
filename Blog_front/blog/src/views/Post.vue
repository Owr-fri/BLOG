<template>
  <div class="home">
    <Header class="header" />
    <div class="post-content">
      <h1>{{ title }}</h1>
      <div class="content">
        <div class="content-html">
          <mavon-editor
            class="md"
            ref="md"
            :value="content"
            :subfield="false"
            :defaultOpen="'preview'"
            :toolbarsFlag="false"
            :shortCut="false"
            :editable="false"
            :ishljs="true"
            @change="dataChange"
          />
        </div>
        <div class="side-nav">
          <div v-for="(item, index) in alink" :key="index">
            <a href="javascript:void(0);" class="nav-link" @click="to(item.id)">
              {{ index + 1 }}.{{ item.name }}
            </a>
          </div>
        </div>
      </div>
      <div class="divide"></div>
      <div class="desc">
        <p>作者:&nbsp; {{ author }}</p>
        <p>
          出处:&nbsp; <a :href="href">{{ href }}</a>
        </p>
        <p>未经授权不得转载</p>
      </div>
      <div class="tags">
        <div class="category">
          <span class="iconfont">&#xe64b;</span>
          <span>分类:</span>
          <a
            href="javascript:void(0)"
            @click="toCategory(category.id, category.name)"
          >
            {{ category.name }}
          </a>
        </div>
        <div class="label">
          <span class="iconfont">&#xe886;</span>
          <span>标签:</span>
          <a
            href="javascript:void(0)"
            v-for="(item, index) in label"
            :key="index"
            @click="toLabel(item.id, item.name)"
          >
            #{{ item.name }}
          </a>
        </div>
        <div class="time">
          <span class="iconfont">&#xe619;</span>
          <span>时间:</span>
          <span> &nbsp;{{ publishTime }} </span>
        </div>
      </div>
      <div class="diggit">
        <div class="dianzan" @click="dianzan" :style="dianzanStyle">
          <span class="iconfont">&#xe600;</span>
        </div>
        <div class="cai" @click="cai" :style="caiStyle">
          <span class="iconfont">&#xea0b;</span>
        </div>
      </div>
      <div class="clear"></div>
      <div class="post_next_prev">
        <div class="prev" v-if="prev.id != -1">
          <span class="prev_span">上一篇:</span>
          <a :href="prev.id"> {{ prev.title }} </a>
        </div>
        <div class="next" v-if="next.id != -1">
          <span class="next_span">下一篇:</span>
          <a :href="next.id"> {{ next.title }} </a>
        </div>
      </div>
      <div class="divide_all"></div>
      <div class="other">
        <span>点赞({{ like_counts }})</span>
        <span class="read-item">阅读({{ read_counts }})</span>
        <span>评论({{ comment_counts }})</span>
      </div>
      <div class="clear"></div>
    </div>

    <div class="comment">
      <div class="comment-list" v-if="commentListShow">
        <h2>评论列表</h2>
        <li
          class="comment-item"
          v-for="(item, index) in comment_list"
          :key="index"
        >
          <div class="flex-block">
            <el-avatar
              shape="square"
              :size="'large'"
              :key="'fit'"
              :src="$API.BASE_SERVER_URL + item.avatar"
            ></el-avatar>
            <div class="comment-content">
              <span class="name">
                {{ item.name }}
              </span>
              <span
                class="del"
                @click="delComment(item.id)"
                v-if="item.userId == userId"
              >
                删除
              </span>
              <div class="clear"></div>
              <div class="feedback">
                {{ item.comment }}
              </div>
            </div>
          </div>
          <div class="comment-desc">
            <span>{{ index + 1 }}楼</span>
            <span>{{ item.time.replace("T", " ") }}</span>
          </div>
          <div class="clear"></div>
          <div class="comment-divide"></div>
        </li>
      </div>
      <div class="put-comment">
        <h2>发布评论</h2>
        <el-form :model="form" :rules="rules" ref="f">
          <el-form-item label="" prop="comment">
            <el-input
              type="textarea"
              placeholder="请输入评论内容"
              v-model="form.comment"
              maxlength="200"
              show-word-limit
              clearable
              :disabled="!islogin"
            >
            </el-input>
          </el-form-item>
        </el-form>
        <el-button
          type="put"
          round
          :size="'mini'"
          class="put-but"
          @click="putComment"
          :loading="commentputting"
          >提交评论</el-button
        >
        <div class="clear"></div>
      </div>
    </div>
    <Footer />
  </div>
</template>

<script>
import Header from "@/components/Header.vue";
import Footer from "@/components/Footer.vue";

export default {
  name: "post",
  components: {
    Header,
    Footer,
  },

  data() {
    return {
      userId: localStorage.getItem("id"),
      postId: "",
      title: "",
      content: "",
      category: "",
      publishTime: "",
      like_counts: "",
      read_counts: "",
      comment_counts: "",
      author: "",
      label: [],
      href: location.origin + location.pathname,
      dianzanStyle: "",
      caiStyle: "",
      dianzanClicked: false,
      caiClicked: false,
      isClicked: false,
      next: "",
      prev: "",
      alink: [],
      comment_list: [],
      commentputting: false,
      form: {
        comment: "",
      },
      rules: {
        comment: [
          { required: true, message: "请输入评论内容", trigger: "blur" },
        ],
      },
    };
  },

  mounted() {
    this.getPost();
    this.getComment();
    setTimeout(() => {
      let formdata = new FormData();
      formdata.append("read_counts", this.read_counts + 1);
      formdata.append("postId", this.postId);
      this.$put(this.$API.API_GET_POST, formdata).then((res) => {
        if (res.code === 200) {
          this.read_counts += 1;
        }
      });
    }, 1000 * 60);
  },
  beforeDestroy() {
    // clearInterval(this.clearTimeSet);
  },

  computed: {
    islogin() {
      return this.userId ? true : false;
    },
    commentListShow() {
      return this.comment_list.length > 0 ? true : false;
    },
  },
  methods: {
    dataChange(value, render) {
      let reg = /<h.?><a id="(.*?)"><.a>(.*?)<.?h.?>/g;
      if (render.match(reg)) {
        render.match(reg).forEach((i) => {
          let id = i.match(/id="(.*?)"/)[1];
          let name = i.match(/<.?a>(.*?)<.?h.?>/)[1];
          this.alink.push({
            id: id,
            name: name,
          });
        });
      }
    },

    getPost() {
      this.$get(this.$API.API_GET_POST, {
        id: this.$route.params["p"],
        userId: localStorage.getItem("id"),
      }).then((res) => {
        if (res.code == 200) {
          this.postId = res.data.id;
          this.title = res.data.title;
          this.content = res.data.content;
          this.author = res.data.author;
          this.category = res.data.category;
          this.label = res.data.label;
          this.publishTime = res.data.publishTime;
          this.next = res.data.next;
          this.prev = res.data.prev;
          this.read_counts = res.data.read_counts;
          this.comment_counts = res.data.comment_counts;
          this.like_counts = res.data.like_counts;
          if (res.data.islike) {
            this.dianzanStyle = "background: #3d615e;color: #f8f8f8;";
            this.dianzanClicked = true;
          }
        } else {
          console.log(res.msg);
        }
      });
    },
    dianzan() {
      if (this.caiClicked) {
        return;
      }
      if (!this.userId) {
        this.$message({
          type: "info",
          message: "请先登录!",
        });
        return;
      }
      if (this.dianzanClicked) {
        this.$del(this.$API.API_LIKE, {
          postId: this.postId,
          userId: this.userId,
        }).then((res) => {
          if (res.code === 200) {
            this.dianzanStyle = "";
            this.dianzanClicked = false;
            this.like_counts -= 1;
            return;
          } else if (res.code === 401) {
            localStorage.clear();
            this.$message({
              message: res.msg,
              type: "error",
            });
            return;
          }
          this.$message.error("取消点赞失败");
        });
        return;
      }

      this.$post(this.$API.API_LIKE, {
        postId: this.postId,
        userId: this.userId,
      }).then((res) => {
        if (res.code === 200) {
          this.dianzanStyle = "background: #3d615e;color: #f8f8f8;";
          this.dianzanClicked = true;
          this.like_counts += 1;
          return;
        }
        this.$message.error("点赞失败");
      });
    },
    cai() {
      if (this.dianzanClicked) {
        return;
      }
      if (!this.userId) {
        this.$message({
          type: "info",
          message: "请先登录!",
        });
        return;
      }
      if (this.caiClicked) {
        this.caiStyle = "";
        this.caiClicked = false;
        return;
      }
      this.caiStyle = "background: #3d615e;color: #f8f8f8;";
      this.caiClicked = true;
    },
    toLabel(id, label) {
      window.sessionStorage.setItem("labelId", id);
      this.$router.push({
        name: "PostByLabel",
        params: {
          name: label,
        },
      });
    },
    toCategory(id, category) {
      window.sessionStorage.setItem("categoryId", id);
      this.$router.push({
        name: "PostByCategory",
        params: {
          name: category,
        },
      });
    },
    to(url) {
      document.querySelector("#" + url).scrollIntoView(true);
    },
    putComment() {
      this.commentputting = true;
      this.$refs["f"].validate((valid) => {
        if (valid) {
          let date = new Date();

          this.$post(this.$API.API_COMMENT, {
            postId: this.postId,
            userId: this.userId,
            time: date.toLocaleDateString() + " " + date.toLocaleTimeString(),
            comment: this.form.comment,
          }).then((res) => {
            if (res.code === 200) {
              let data = res.data;
              this.comment_list.unshift({
                comment: data.comment,
                id: data.id,
                userId: data.userId,
                postId: data.postId,
                name: localStorage.getItem("name"),
                avatar: localStorage.getItem("avatar"),
                time: data.time.replace("T", " "),
              });
              this.form.comment = "";
              this.commentputting = false;
              return;
            } else if (res.code === 401) {
              localStorage.clear();
              this.$message({
                message: res.msg,
                type: "error",
              });
              return;
            }
            this.$message.error("提交失败");
          });
        } else {
          this.commentputting = false;
          return false;
        }
      });
    },
    getComment() {
      this.$get(this.$API.API_COMMENT, {
        postId: this.$route.params["p"],
      }).then((res) => {
        this.comment_list = res.data;
      });
    },
    delComment(id) {
      this.$del(this.$API.API_COMMENT, {
        id: id,
      }).then((res) => {
        if (res.code === 200) {
          this.comment_list = this.comment_list.filter((i) => {
            return i.id != id;
          });
          this.$message({
            type: "success",
            message: "删除成功!",
          });
        } else if (res.code === 401) {
          localStorage.clear();
          this.$message({
            message: res.msg,
            type: "error",
          });
        } else {
          this.$message({
            type: "error",
            message: "删除失败!",
          });
        }
      });
    },
  },
};
</script>

<style lang="less" scoped>
.home {
  margin: 0px auto;
  width: 920px;
  min-height: 100%;
}

.footer {
  margin: 0px auto;
  width: 920px;
  height: 45px;
  bottom: 0px;
}

.post-content {
  margin-top: 15px;
  min-height: calc(90vh);
  width: 100%;
}

h1 {
  margin-bottom: 10px;
  font-size: 21px;
  color: #464a4a;
}

.divide {
  display: block;
  width: 60%;
  margin: 20px 0 20px 97px;
  // margin: 20px auto;
  // width: 70%;
  border-bottom: 1px solid #e8ecf1;
}

.divide_all {
  width: 100%;
  border-bottom: 1px solid #e8ecf1;
}

.clear {
  clear: both;
}

.other {
  float: right;
  font-size: 12px;
  font-weight: 200;
  color: #464a4a;

  span {
    margin-left: 3px;
  }
}

.post_next_prev {
  font-size: 12px;
  font-weight: 200;
  margin-bottom: 5px;

  span {
    line-height: 1.5;
  }

  .prev_span::before {
    content: "\00AB";
  }

  .next_span::before {
    content: "\00bb";
  }

  a {
    position: relative;
    color: #456795;
    margin-left: 5px;
    display: inline-block;
  }

  a::after {
    content: "";
    display: block;
    width: 100%;
    height: 0.1px;
    position: absolute;
    left: 0;
    background: #456795;
    transform: scaleX(0);
    transform-origin: left;
    transition: all 0.3s ease-in-out;
  }

  a:hover::after {
    transform: scaleX(1);
  }
}

.diggit {
  margin: 20px 0 5px 0;
  float: right;
  cursor: pointer;

  .dig-dianzan,
  .dig-cai {
    font-size: 14px;
    margin-left: 2px;
  }

  .iconfont {
    font-size: 16px;
    font-weight: 200;
  }

  .dianzan,
  .cai {
    color: #464a4a;
    display: inline-block;
    width: 60px;
    text-align: center;
    background: #f8f8f8;
    padding: 4px 3px 4px 0;
    border-radius: 5px;
    transition: all 0.3s ease;
  }

  .dianzan {
    margin-right: 10px;
  }

  .dianzan:hover,
  .cai:hover {
    background: #3d615e;
    color: #f8f8f8;
    transition: all 0.3s ease;
  }
}

.desc {
  background: #f8f8f8;
  border-radius: 3px;
  margin: 0 auto;
  margin-bottom: 10px;
  padding: 12px 24px 12px 20px;
  border-left: 4px solid #2b6964;

  p {
    font-size: 13px;
    color: #3d615e;
    line-height: 1.5;
    font-weight: 200;
  }

  a {
    display: inline-block;
    position: relative;
  }

  a::after {
    content: "";
    display: block;
    width: 100%;
    height: 0.1px;
    position: absolute;
    left: 0;
    background: #3d615e;
    transform: scaleX(0);
    transform-origin: left;
    transition: all 0.3s ease-in-out;
  }

  a:hover::after {
    height: 0.1px;
    transform: scaleX(1);
  }
}

.tags {
  margin-top: 15px;
  color: #464a4a;
  opacity: 0.8;
  font-weight: 200;
  line-height: 1;
  vertical-align: middle;
  font-size: 12px;

  .iconfont {
    font-size: 12px;
    margin: 0 5px;
  }

  a {
    font-weight: 100;
    display: inline-block;
    margin-left: 7px;
    color: #464a4a;
    background: #f8f8f8;
    padding: 4px 6px;
    border-radius: 3px;
  }

  a:hover {
    background: #3d615e;
    color: white;
  }

  .category,
  .label {
    margin-bottom: 5px;
  }
}

.side-nav {
  position: sticky;
  margin-left: 15px;
  height: 200px;
  top: 20px;
  overflow: hidden;

  .nav-link {
    display: inline-block;
    font-size: 12px;
    font-weight: 200;
    color: black;
    line-height: 1.5;
    margin-top: 4px;
    vertical-align: middle;
  }
}

.content {
  width: 100%;
  display: flex;
}

.content-html {
  min-height: calc(50vh);
  padding: 0 10px 0 0;
  border-right: 1px solid #e8ecf1;
  width: 85%;

  /deep/ h1 {
    font-size: 21px;
    color: #464a4a;
  }

  /deep/ h2 {
    font-size: 20px;
    margin-bottom: 10px;
    color: #464a4a;
  }

  /deep/ h3 {
    margin: 10px 0px;
    font-size: 18px;
    color: #464a4a;
    cursor: pointer;
    display: inline-block;
  }

  /deep/ img {
    overflow: hidden;
    max-width: 720px;
    display: block;
    margin: 5px 0;
    border-radius: 3px;
    box-shadow: 1px 1px 2px #5c5c5c94;
    width: 100%;
  }

  /deep/ p {
    font-size: 14px;
    font-weight: 200;
    line-height: 1.5;
  }

  /deep/ h3::after {
    content: "";
  }

  /deep/ h3:hover::after {
    content: "#";
    color: #456795;
    height: 0px;
    position: absolute;
    animation: fade-in 0.5s cubic-bezier(0.39, 0.575, 0.565, 1) both;
  }

  @keyframes fade-in {
    0% {
      opacity: 0;
    }

    100% {
      opacity: 1;
    }
  }

  /deep/ p a {
    color: #456795;
    text-decoration: none;
  }

  /deep/ p a::after {
    content: "";
    display: block;
    width: 100%;
    height: 1px;
    position: absolute;
    left: 0;
    bottom: -1px;
    background: #456795;
    transform: scaleX(0);
    transform-origin: left;
    transition: all 0.3s ease-in-out;
  }

  /deep/ p a:hover::after {
    transform: scaleX(1);
  }

  /deep/ p a {
    margin-left: 5px;
    display: inline-block;
    position: relative;
    text-align: center;
  }
}
.comment-list {
  margin: 20px 0;
  h2 {
    font-size: 16px;
    font-weight: 300;
    padding-bottom: 7px;
    border-bottom: 1px solid #e8ecf1;
    margin-bottom: 15px;
  }
}
.put-comment {
  margin: 20px 0;
  h2 {
    font-size: 16px;
    font-weight: 300;
    padding-bottom: 7px;
  }
}
.put-but {
  float: right;
}
/deep/.el-textarea__inner:focus {
  border-color: #2b6964c9;
}
/deep/.el-form-item {
  margin-bottom: 8px;
}
.el-button--put.is-active,
.el-button--put:active {
  background: #2b6964c9;
  border-color: #2b6964c9;
  color: #fff;
}

.el-button--put:focus,
.el-button--put:hover {
  background: #2b6964c9;
  border-color: #2b6964c9;
  color: #fff;
}

.el-button--put {
  color: #fff;
  background-color: #2b6964;
  border-color: #2b6964;
}
.comment-item {
  list-style: none;
  font-size: 12px;
  font-weight: 300;
  margin-bottom: 5px;
}
.flex-block {
  display: flex;
}
.comment-content {
  padding-left: 4px;
  .name {
    font-size: 13px;
    font-weight: 400;
    color: #409b93;
  }
  .feedback {
    margin-top: 3px;
    width: 850px;
    padding: 8px 8px;
    background: #f8f8f8;
    border-radius: 3px;
    border-left: 3px solid #2b6964;
  }
}
.comment-desc {
  float: right;
  margin-top: 2px;
  font-weight: 200;
  vertical-align: baseline;
  margin-bottom: 10px;
  font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
  span {
    line-height: 1.2;
    display: inline-block;
    margin: 0 4px;
    color: #999;
  }
}
.comment-divide {
  width: 80%;
  margin: 0 auto;
  border-top: 1px solid #e8ecf1;
}
.del {
  float: right;
  color: red;
  cursor: pointer;
}
</style>
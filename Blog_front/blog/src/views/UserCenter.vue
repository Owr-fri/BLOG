<template>
  <div class="userCenter">
    <Header />
    <div class="main">
      <div class="info">
        <i class="el-icon-switch-button" @click="logout"></i>
        <div class="left">
          <div class="avatar-center">
            <div class="avatar-item">
              <el-upload
                class="avatar-uploader"
                v-if="isEdit"
                :action="$API.API_AVATAR"
                :show-file-list="false"
                :on-success="handleAvatarSuccess"
                accept=".jpg,.jpeg,.png,.gif.JPG,.JPEG,.PNG,.GIF"
              >
                <img
                  v-if="avatar"
                  :src="$API.BASE_SERVER_URL + avatar"
                  class="avatar"
                />
              </el-upload>
              <img
                v-if="avatar && !isEdit"
                :src="$API.BASE_SERVER_URL + avatar"
                class="avatar"
              />
            </div>
          </div>
          <div class="center">
            <span style="font-size: 19px">{{ name }}</span>
            <div class="role">
              <i class="el-icon-user"></i>
              {{ role }}
            </div>
          </div>
          <div class="divide"></div>
          <div class="email">
            <span class="iconfont email-font">&#xe612;</span>
            {{ email }}
          </div>
        </div>
        <div class="right">
          <div class="vertical-divide"></div>
          <div class="desc">
            <el-descriptions title="用户信息" :column="3" :size="'large'">
              <template slot="extra">
                <i
                  class="el-icon-edit"
                  @click="edit"
                  v-if="!isEdit & !updateLoading"
                ></i>
                <i
                  class="el-icon-check"
                  @click="update"
                  v-else-if="isEdit & !updateLoading"
                ></i>
                <i class="el-icon-loading" v-else-if="updateLoading"></i>
              </template>
              <el-descriptions-item label="用户名">
                <el-input
                  v-model="name"
                  placeholder="用户名"
                  v-if="isEdit"
                  :size="'mini'"
                ></el-input>
                <span v-else>{{ name }}</span>
              </el-descriptions-item>
              <el-descriptions-item label="手机号"
                ><el-input
                  v-model="phone"
                  placeholder="手机号"
                  v-if="isEdit"
                  :size="'mini'"
                ></el-input
                ><span v-else>{{ phone }}</span></el-descriptions-item
              >
              <el-descriptions-item label="邮箱"
                ><span>{{ email }}</span></el-descriptions-item
              >
              <el-descriptions-item label="登录时间"
                ><span>{{ loginTime }}</span></el-descriptions-item
              >
              <el-descriptions-item label="用户身份">{{
                Crole
              }}</el-descriptions-item>
            </el-descriptions>
          </div>
          <div class="divide"></div>
          <div class="jianyan">
            <span> 请遵守用户规范 </span>
          </div>
        </div>
      </div>
      <div class="commented-post">
        <div class="bottom-line">
          <h2 class="commented-title">{{ name }}的评论</h2>
        </div>
        <div class="commented-list">
          <el-timeline>
            <el-timeline-item
              :timestamp="item.time.replace('T', ' ')"
              placement="top"
              v-for="item in commentList"
              :key="item.id"
              :color="'#3fc9be'"
            >
              <el-card>
                <h4>博客: {{ item.title }}</h4>
                <span class="del" @click="delComment(item.id)">删除</span>
                <div class="clear"></div>
                <p>评论内容: {{ item.comment }}</p>
              </el-card>
            </el-timeline-item>
          </el-timeline>
        </div>
      </div>
      <div class="liked-post">
        <div class="bottom-line">
          <h2 class="liked-title">{{ name }}的点赞</h2>
        </div>
        <div class="liked-list">
          <el-timeline>
            <el-timeline-item
              :hide-timestamp="true"
              v-for="item in likeList"
              :key="item.id"
              :color="'#3fc9be'"
            >
              <el-card>
                <h4>已点赞博客: {{ item.title }}</h4>
                <el-button
                  class="del"
                  type="danger"
                  size="mini"
                  @click="cancelLike(item.id)"
                  plain
                  >取消点赞</el-button
                >
                <div class="clear"></div>
              </el-card>
            </el-timeline-item>
          </el-timeline>
        </div>
      </div>
    </div>
    <Footer />
  </div>
</template>

<script>
import Header from "@/components/Header.vue";
import Footer from "@/components/Footer.vue";

export default {
  name: "user-center",
  components: {
    Header,
    Footer,
  },
  data() {
    return {
      id: window.localStorage.getItem("id"),
      name: "",
      email: "",
      avatar: "",
      loginTime: "",
      role: "",
      phone: "",
      commentList: [],
      isEdit: false,
      likeList: [],
      updateLoading: false,
    };
  },
  computed: {
    Crole() {
      if (this.role == "s") {
        return "管理员";
      }
      if (this.role == "u") {
        return "用户";
      }
      return "访客";
    },
  },
  beforeMount() {},
  mounted() {
    this.getUserInfo();
    this.getCommentList();
    this.getLike();
  },
  methods: {
    getUserInfo() {
      if (this.id) {
        this.$get(this.$API.API_USER_INFO, {
          id: this.id,
        }).then((res) => {
          this.name = res.data.name;
          this.email = res.data.email;
          this.avatar = res.data.avatar;
          this.role = res.data.role;
          this.phone = res.data.phone;
          this.loginTime = res.data.loginTime;
        });
      }
    },
    edit() {
      this.isEdit = true;
    },
    update() {
      if (this.phone !== "") {
        let reg = /^((0\d{2,3}-\d{7,8})|(1[3584]\d{9}))$/;
        if (!reg.test(this.phone)) {
          this.$message({
            message: "请输入正确的手机号",
            type: "info",
          });
          return;
        }
      }

      this.updateLoading = true;
      var formdata = new FormData();
      formdata.append("id", this.id);
      formdata.append("name", this.name);
      formdata.append("phone", this.phone);
      formdata.append("avatar", this.avatar);
      this.$put(this.$API.API_USER_INFO, formdata).then((res) => {
        this.updateLoading = false;
        if (res.code === 200) {
          localStorage.setItem("name", this.name);
          localStorage.setItem("avatar", this.avatar);
          this.isEdit = false;
        } else if (res.code === 401) {
          this.$message({
            message: res.msg,
            type: "error",
          });
        } else {
          this.$message({
            message: "修改失败",
            type: "error",
          });
        }
      });
    },
    logout() {
      this.$get(this.$API.API_LOGIN).then((res) => {
        if (res) {
          localStorage.clear();
          this.$router.push("/");
        }
      });
    },
    handleAvatarSuccess(res) {
      this.avatar = res.data.avatar;
    },
    getCommentList() {
      this.$get(this.$API.API_COMMENT, {
        userId: localStorage.getItem("id"),
      }).then((res) => {
        this.commentList = res.data;
      });
    },
    delComment(id) {
      this.$del(this.$API.API_COMMENT, {
        id: id,
      }).then((res) => {
        if (res.code === 200) {
          this.commentList = this.commentList.filter((i) => {
            return i.id != id;
          });
        } else {
          this.$message({
            message: res.msg,
            type: "error",
          });
        }
      });
    },
    getLike() {
      this.$get(this.$API.API_LIKE, {
        id: localStorage.getItem("id"),
      }).then((res) => {
        this.likeList = res.data;
        console.log(this.likeList);
      });
    },
    cancelLike(id) {
      this.$del(this.$API.API_LIKE, {
        id: id,
      }).then((res) => {
        if (res.code === 200) {
          this.likeList = this.likeList.filter((i) => {
            return i.id != id;
          });
        } else {
          this.$message({
            message: res.msg,
            type: "error",
          });
        }
      });
    },
  },
};
</script>

<style lang='less' scoped>
.userCenter {
  margin: 0px auto;
  width: 920px;
  height: 100%;
}
.main {
  margin-top: 15px;
  min-height: calc(81vh);
}
.info,
.commented-post,
.liked-post {
  width: 900px;
  padding: 8px 10px 10px 8px;
  border-radius: 4px;
  border: 1px solid #e8ecf1;
  border-radius: 5px;
  box-shadow: 0 0 8px rgba(0, 0, 0, 0.1);
}
.info {
  display: flex;
  height: 180px;
}
.commented-post,
.liked-post {
  height: 250px;
}
.el-avatar--large {
  width: 60px !important;
  height: 60px !important;
  line-height: 60px !important;
}
.el-avatar {
  cursor: pointer;
  box-shadow: 0 0 8px rgba(0, 0, 0, 0.3);
}
.avatar {
  margin-top: 20px;
  display: block;
  text-align: center;
  position: relative;
}
.left {
  width: 30%;
}
.right {
  width: 70%;
}
.center {
  text-align: center;
  // padding-top: 2px;
  span {
    color: #000000a1;
  }
  .role {
    color: #00000045;
    font-size: 12px;
    font-weight: 400;
    margin-top: 2px;
  }
}
.divide {
  margin: 0 auto;
  width: 70%;
  margin-top: 10px;
  border-top: 1px solid #e8ecf1;
}
.email {
  padding-top: 4px;
  text-align: center;
  color: #000000a1;
  font-size: 12px;
  font-weight: 400;
  margin-top: 2px;
  .email-font {
    font-size: 12px;
    padding-right: 2px;
  }
}
.vertical-divide {
  float: left;
  margin-top: 15px;
  height: 80%;
  border-left: 1px solid #e8ecf1;
}
.desc {
  padding-left: 20px;
  padding-top: 10px;
  margin-bottom: 25px;
  h2 {
    font-size: 14px;
    margin-bottom: 15px;
  }
}
.jianyan {
  margin-top: 7px;
  text-align: center;
  font-size: 12px;
  font-weight: 200;
}
.el-icon-edit:before,
.el-icon-check:before,
.el-icon-switch-button:before {
  cursor: pointer;
  font-size: 18px;
  margin-right: 10px;
}
.el-icon-loading:before {
  cursor: pointer;
  font-size: 18px;
}
.el-icon-check:before {
  color: #00aeff;
}
.el-icon-switch-button:before {
  color: #d71f1fc7;
}
/deep/.el-input--mini .el-input__inner {
  height: 29px;
  width: 135px;
  line-height: 29px;
}
.el-icon-loading {
  margin-right: 10px;
}
/deep/.el-descriptions__body
  .el-descriptions__table
  .el-descriptions-item__cell {
  line-height: 2.3;
}
/deep/.el-descriptions :not(.is-bordered) .el-descriptions-item__cell {
  padding-bottom: 5px;
}
/deep/.el-input__inner {
  font-size: 14px;
  padding: 0 0px;
}
.avatar {
  width: 60px;
  height: 60px;
  margin-top: 13px;
  display: inline-block;
  border-radius: 50%;
}
/deep/ .el-upload {
  display: inline-block;
  border-radius: 50%;
}
.avatar-item {
  display: inline-block;
  margin: 0 auto;
}
.avatar-center {
  text-align: center;
}
.commented-post,
.liked-post {
  margin-top: 15px;
  padding-left: 10px;
}
.commented-title,
.liked-title {
  font-size: 14px;
  position: relative;
  display: inline-block;
  margin-left: 10px;
}
.commented-title::before {
  content: "";
  display: block;
  width: 100%;
  height: 3px;
  position: absolute;
  bottom: -7px;
  left: 0;
  background-color: #3fc9be;
}

.liked-title::before {
  content: "";
  display: block;
  width: 100%;
  height: 3px;
  position: absolute;
  bottom: -7px;
  left: 0;
  background-color: #3fc9be;
}
.bottom-line {
  padding-bottom: 6px;
  border-bottom: 1px solid #e8ecf1;
}
.commented-list,
.liked-list {
  padding-left: 10px;
  margin-top: 20px;
  overflow-y: auto;
  max-height: 200px;
  h4 {
    display: inline-block;
    line-height: 2;
  }
}
/deep/.el-timeline-item {
  padding-bottom: 10px;
}
/deep/.el-card__body {
  padding: 15px;
}
.el-timeline {
  width: 90%;
}
.del {
  float: right;
  cursor: pointer;
  color: red;
  font-size: 12px;
  font-weight: 200;
}
.clear {
  clear: both;
}
</style>
<template>
  <div class="home">
    <Header />
    <div class="main">
      <div class="nav-bar">
        <el-row class="tac">
          <el-col :span="4">
            <el-menu
              :default-active="this.$route.path"
              class="menu-bar"
              active-text-color="#3fc9be"
              text-color="#505560"
              :router="true"
            >
              <el-submenu index="posts-manage">
                <template slot="title">
                  <span>博客管理</span>
                </template>
                <el-menu-item-group>
                  <el-menu-item index="/manage/ppost">发布博客</el-menu-item>
                  <el-menu-item index="/manage/mpost">管理博客</el-menu-item>
                </el-menu-item-group>
              </el-submenu>
              <el-submenu index="picture-manage">
                <template slot="title">
                  <span>图集管理</span>
                </template>
                <el-menu-item-group>
                  <el-menu-item index="/manage/ppicture">发布图集</el-menu-item>
                  <el-menu-item index="/manage/mpicture">管理图集</el-menu-item>
                </el-menu-item-group>
              </el-submenu>
              <el-submenu index="author-manage">
                <template slot="title">
                  <span>个人管理</span>
                </template>
                <el-menu-item-group>
                  <el-menu-item index="/manage/picp">更改个人信息</el-menu-item>
                  <el-menu-item index="/manage/picp">更改个人信息</el-menu-item>
                  <el-menu-item index="/manage/picp">更改个人信息</el-menu-item>
                </el-menu-item-group>
              </el-submenu>
            </el-menu>
          </el-col>
        </el-row>
      </div>
      <div class="activate-content">
        <el-empty
          :description="description"
          v-if="this.$route.path == '/manage'"
        ></el-empty>
        <router-view></router-view>
      </div>
      <div class="clear"></div>
    </div>

    <Footer />
  </div>
</template>

<script>
import Header from "@/components/Header.vue";
import Footer from "@/components/Footer.vue";

export default {
  name: "editor",
  components: {
    Header,
    Footer,
  },
  data() {
    return {
      description: "请选择导航",
    };
  },
  beforeMount() {
    this.$get(this.$API.API_IS_ADMIN).then((res) => {
      if (res.code === 200) {
        return;
      }
      if (res.code === 303) {
        this.$confirm(res.msg, "提示", {
          confirmButtonText: "确定",
          type: "warning",
          closeOnClickModal: false,
          closeOnPressEscape: false,
          closeOnHashChange: false,
          center: true,
          showCancelButton: false,
          showClose: false,
        }).then(() => {
          this.$router.push("/");
        });
        return;
      }
      this.$router.push("/");
    });
  },
  mounted() {},
};
</script>

<style scoped>
.home {
  margin: 0px auto;
  height: 100%;
  width: 920px;
}

.el-menu-item {
  min-width: 155px !important;
}

.footer {
  margin: 0px auto;
  width: 940px;
  height: 45px;
  bottom: 0px;
}

.main {
  margin-top: 15px;
  min-height: calc(90vh);
}

.nav-bar {
  width: 155px;
  float: left;
}

.nav-bar >>> .el-col-4 {
  width: 100% !important;
}

.activate-content {
  width: 82%;
  float: right;
}

.clear {
  clear: both;
}
</style>
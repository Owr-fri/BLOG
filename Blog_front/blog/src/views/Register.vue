<template>
  <div class="login-main">
    <div class="login">
      <h2 class="login-title">注册</h2>
      <hr align="center" width="50%" style="margin-bottom: 0px" />
      <div class="login-content">
        <font style="font-family: STXingkai">user login</font>
        <form actio style="padding-top: 40px">
          <div class="name-item">
            <span class="icon iconfont icon-yonghu"></span>
            <input
              type="text"
              class="name-input"
              name=""
              id="name"
              v-model="form.name"
              placeholder="用户名"
            />
          </div>
          <div class="user-item">
            <span class="iconfont">&#xea0c;</span>
            <input
              type="text"
              class="user-input"
              name=""
              id="email"
              v-model="form.email"
              placeholder="邮箱"
            />
          </div>
          <div class="pwd-item">
            <span class="icon iconfont icon-mima1"></span>
            <input
              type="password"
              class="pwd-input"
              name=""
              id="pwd"
              v-model="form.pwd"
              placeholder="密码"
            />
          </div>
          <div class="comfirm-item">
            <span class="comfirm">确认密码</span>
            <input
              type="password"
              class="comfirm-input"
              name=""
              id="comfirm"
              v-model="form.comfirm"
              placeholder="确认密码"
            />
          </div>
        </form>
        <div class="submit-but">
          <span class="icon iconfont icon-queren" @click="Submit()"></span>
        </div>
        <a href="/login" class="tologin">登录<i class="el-icon-right"></i></a>
      </div>
    </div>
  </div>
</template>

<script>
// import axios from 'axios';

export default {
  name: "login",
  data() {
    return {
      form: {
        email: "431306642@qq.com",
        pwd: "020706",
        name: "user1",
        comfirm: "020706",
      },
    };
  },
  methods: {
    getCode() {
      let f = this.checkEmailNull(this.form.email);
      if (f) {
        this.$get(this.$API.API_GET_CODE, {
          email: this.form.email,
        }).then((res) => {
          console.log(res);
        });
      }
    },
    Submit() {
      let f = false;
      if (this.checkEmailNull(this.form.email)) {
        if (this.checkPwd(this.form.pwd)) {
          if (this.comfirmPwd(this.form.pwd, this.form.comfirm)) {
            if (this.checkName(this.form.name)) {
              f = true;
            }
          }
        }
      }
      if (f) {
        console.log("注册");
        this.$post(this.$API.API_REGISTER, {
          name: this.form.name,
          pwd: this.form.pwd,
          comfirm: this.form.comfirm,
          email: this.form.email,
        }).then((res) => {
          if (res.code === 200) {
            this.$notify({
              title: "成功",
              message: "注册成功",
              type: "success",
            });
          }else{
            this.$notify({
              title: "失败",
              message: "注册失败",
              type: "error",
            });
          }
        });
      }
    },
    checkEmailNull(email) {
      if (email.length == 0) {
        const h = this.$createElement;
        this.$notify({
          title: "邮箱错误",
          message: h("i", { style: "color: teal" }, "邮箱不可为空"),
          showClose: false,
        });
        return false;
      }
      const reg =
        /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
      if (reg.test(email)) {
        return true;
      } else {
        const h = this.$createElement;
        this.$notify({
          title: "邮箱错误",
          message: h("i", { style: "color: teal" }, "错误的邮箱格式"),
          showClose: false,
        });
        return false;
      }
    },
    checkPwd(pwd) {
      const h = this.$createElement;
      if (pwd.length == 0) {
        this.$notify({
          title: "密码错误",
          message: h("i", { style: "color: teal" }, "密码不能为空"),
          showClose: false,
        });
        return false;
      } else if ((pwd.length < 6) | (pwd.length > 16)) {
        this.$notify({
          title: "密码错误",
          message: h("i", { style: "color: teal" }, "密码长度为6-16"),
          showClose: false,
        });
        return false;
      }
      return true;
    },
    checkVerifyNull(verify) {
      const h = this.$createElement;
      if (verify.length == 0) {
        this.$notify({
          title: "验证码错误",
          message: h("i", { style: "color: teal" }, "验证码不能为空"),
          showClose: false,
        });
        return false;
      }
      return true;
    },
    comfirmPwd(pwd, comfirm) {
      if (pwd == comfirm) {
        return true;
      }
      const h = this.$createElement;
      this.$notify({
        title: "密码验证错误",
        message: h("i", { style: "color: teal" }, "两次输入的密码不同"),
        showClose: false,
      });
      return false;
    },
    checkName(name) {
      if (name.length != 0) {
        if (name.length > 15) {
          const h = this.$createElement;
          this.$notify({
            title: "用户名错误",
            message: h("i", { style: "color: teal" }, "用户名长度不可超过15"),
            showClose: false,
          });
          return false;
        }
        return true;
      }
      const h = this.$createElement;
      this.$notify({
        title: "用户名错误",
        message: h("i", { style: "color: teal" }, "请输入用户名"),
        showClose: false,
      });
      return false;
    },
  },
};
</script>

<style scoped lang='less'>
.login-main {
  text-align: center;
  display: flex;
  width: 100%;
  height: 100vh;
  align-items: center;
  justify-content: center;
  background: url("~@/common/images/banner1_01.jpg");
  background-position: center;
  background-size: cover;
}

body {
  margin: 0px;
  padding: 0px;
  position: fixed;
  width: 100%;
  height: 100%;
  background-position: center;
  background-size: cover;
}

.login {
  width: 350px;
  height: 450px;
  background: white;
  border-radius: 6px;
  box-shadow: 2px 2px 10px #5c5c5c;
}

.login-title {
  margin-bottom: 0px;
  padding-top: 30px;
}

.user-item,
.pwd-item,
.name-item,
.comfirm-item {
  height: 35px;
  margin: 0 auto;
  border: 1px solid #e3e8f0;
  width: 75%;
  vertical-align: top;
  box-sizing: border-box;
  border-radius: 15px;
  margin-bottom: 24px;
}

.user-input,
.pwd-input,
.name-input,
.comfirm-input {
  height: 30px;
  border: none;
  outline: none;
  padding-left: 20px;
  height: 33px;
}

.icon-yonghu {
  font-size: 1.2em;
  vertical-align: middle;
}

.icon-mima {
  font-size: 1em;
  vertical-align: middle;
}

.icon-queren:before {
  font-size: 2.5em;
  color: #3fc9be;
  cursor: pointer;
}

hr {
  margin-left: auto;
  margin-right: auto;
  width: 50%;
}
.tologin {
  float: right;
  margin-top: 20px;
  margin-right: 15px;
  font-size: 12px;
  font-weight: 200;
}
.comfirm {
  font-size: 12px;
  font-weight: 200;
}
</style>
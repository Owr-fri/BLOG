<template>
  <div class="login-main">
    <div class="login">
      <h2 class="login-title">登录</h2>
      <hr align="center" width="50%" style="margin-bottom: 0px" />
      <div class="login-content">
        <font style="font-family: STXingkai">user login</font>
        <!-- <span class="icon iconfont icon-mimabukejian"></span> -->
        <!-- 用户登录  -->
        <form actio style="padding-top: 40px">
          <div class="user-item">
            <!-- <span class="icon iconfont icon-yonghu"></span> -->
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
          <div class="email-item">
            <div class="email-verify">
              <input
                type="text"
                class="verify-input"
                autocomplete="off"
                maxlength="4"
                name=""
                id="ver"
                v-model="form.verify"
                placeholder="验证码"
              />
            </div>
            <div>
              <button type="button" class="send-but" @click="getCode()">
                获取验证码
              </button>
            </div>
          </div>
        </form>
        <div class="submit-but">
          <span class="icon iconfont icon-queren" @click="Submit()"></span>
        </div>
        <a href="/register" class="register"
          >注册 <i class="el-icon-right"></i
        ></a>
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
        verify: "1865",
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
          if (this.checkVerifyNull(this.form.verify)) {
            f = true;
          }
        }
      }
      if (f) {
        let date = new Date();
        this.$post(this.$API.API_LOGIN, {
          pwd: this.form.pwd,
          username: this.form.email,
          verify: this.form.verify,
          time: date.toLocaleDateString(),
        }).then((res) => {
          if (res.code == 200) {
            window.localStorage.setItem("id", res.data.id);
            window.localStorage.setItem("name", res.data.name);
            window.localStorage.setItem("avatar", res.data.avatar);
            window.localStorage.setItem("role", res.data.role);
            this.$router.push("/");
          } else {
            this.$message({
              message: "登陆失败",
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
  height: 400px;
  background: white;
  border-radius: 6px;
  box-shadow: 2px 2px 10px #5c5c5c;
}

.login-title {
  margin-bottom: 0px;
  padding-top: 30px;
}

.user-item,
.pwd-item {
  height: 35px;
  margin: 0 auto;
  border: 1px solid #e3e8f0;
  width: 75%;
  vertical-align: top;
  box-sizing: border-box;
  border-radius: 15px;
  margin-bottom: 24px;
}

.email-verify {
  float: left;
  width: 120px;
  margin-left: 44px;
}

.user-input,
.pwd-input {
  height: 30px;
  border: none;
  outline: none;
  padding-left: 20px;
  height: 33px;
}

.email-item {
  height: 35px;
  margin-bottom: 24px;
}

.verify-input {
  border: 1px solid #e3e8f0;
  box-sizing: border-box;
  height: 35px;
  border-radius: 15px;
  outline: none;
  text-align: center;
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

.send-but {
  height: 35px;
  background: #3fc9be;
  border-radius: 15px;
  border: none;
  color: white;
  width: 25%;
  margin-left: 10px;
  transition: all 0.1s linear;
  cursor: pointer;
}
.send-but:hover {
  box-shadow: 0px 0px 2px 0px #5c5c5c;
}

hr {
  margin-left: auto;
  margin-right: auto;
  width: 50%;
}
.register {
  float: right;
  margin-top: 25px;
  margin-right: 15px;
  font-size: 12px;
  font-weight: 200;
}
</style>
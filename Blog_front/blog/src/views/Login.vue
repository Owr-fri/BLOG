<template>
  <div class="login-main">
      <div class="login">
          <h2 class="login-title">登录</h2>
          <hr align="center" width="50%" style="margin-bottom: 0px;">
          <div class="login-content">
            <font style="font-family:STXingkai">user login</font>
            <!-- <span class="icon iconfont icon-mimabukejian"></span> -->
            <!-- 用户登录  -->
            <form actio style="padding-top: 40px;">
                <div class="user-item">
                  <span class="icon iconfont icon-yonghu"></span>
                  <input type="text" class="user-input" name="" id="phone" v-model="form.phone" placeholder="邮箱/登录账号">
                </div>
                <div class="pwd-item">
                  <span class="icon iconfont icon-mima1"></span>
                  <input type="password" class="pwd-input" name="" id="pwd" v-model="form.pwd" placeholder="密码">
                </div>
                <div class="email-item">
                  <div class="email-verify">
                    <input type="text" class="verify-input" name="" id="ver" v-model="form.verify" placeholder="验证码">
                  </div>
                  <div>
                    <button class="send-but" @click="getCode()">获取验证码</button>
                  </div>
                </div>
            </form>
            <div class="submit-but">
                  <span class="icon iconfont icon-queren"></span>
            </div>
          </div>
      </div>
  </div>
</template>

<script>
export default {
  name: 'login',
  data(){
    return {
      form:{
        phone:"12312",
        pwd:"",
        verify:""
      }
    }
  },
  methods:{
    getCode(){
      this.$http.get(
        this.$API.API_GET_CODE,{
          params:{
            email:this.form.email
          }
        }).then(res => {
          console.log(res)
        })
    },
  }
}
</script>

<style>
    .login-main{
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
      position:fixed;
      width: 100%;
      height:100%;
      background-position: center;
      background-size: cover;
    }
    .login{
      width: 350px;
      height: 400px;
      background: white;
      border-radius: 6px;
      box-shadow: 2px 2px 10px #5c5c5c;
    }
    .login-title{
      margin-bottom: 0px;
      padding-top: 30px;
    }
    .user-item,.pwd-item{
      height: 35px;
      margin:0 auto;
      border: 1px solid #E3E8F0;
      width: 75%;
      vertical-align: top;
      box-sizing: border-box;
      border-radius: 15px;
      margin-bottom: 24px;
    }
    .email-verify{
      float: left;
      width: 120px;
      margin-left: 44px;
    }
    .user-input,.pwd-input{
      height: 30px;
      border: none;
      outline:none;
      padding-left: 20px;
    }
    .email-item{
      height: 35px;
      margin-bottom: 24px;
    }
    .verify-input{
      border: 1px solid #E3E8F0;
      box-sizing: border-box;
      height: 35px;
      border-radius: 15px;
      outline:none;
      text-align: center;
    }
    .icon-yonghu{
      font-size: 1.2em;
      vertical-align: middle;
    }
    .icon-mima{
      font-size: 1em;
      vertical-align: middle;
    }
    .icon-queren:before{
      font-size: 2.5em;
      color: #3fc9be;
    }
    .send-but{
      height: 35px;
      background: #3fc9be;
      border-radius: 15px;
      border: none;
      color: white;
      width: 25%;
      margin-left: 10px;
    }

</style>

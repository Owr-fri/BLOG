import Vue from 'vue'
import App from './App.vue'
import router from "./router"
import './assets/icon/iconfont.css'
import axios from 'axios'
import API from "./common/js/APIUtil"


Vue.config.productionTip = false

// axios赋值给变量axios
Vue.prototype.$http = axios
Vue.prototype.$url = "http://127.0.0.1:8000/"
Vue.prototype.$API = API

new Vue({
  axios,
  router,
  render: h => h(App),
}).$mount('#app')

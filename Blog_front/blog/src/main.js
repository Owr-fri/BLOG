import Vue from 'vue'
import App from './App.vue'
// 导入router
import router from "./router"
// 导入element
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
// 导入iconfont
import './assets/icon/iconfont.css'
// 导入axios
// import axios from 'axios'
import axios from './common/js/axios'
// 导入API
import API from "./common/js/APIUtil"
// 导入qs
import qs from 'qs'
// 导入fetch
import fetch from './common/js/fetch'

Vue.config.productionTip = false

Vue.use(ElementUI);

// axios赋值给变量axios
Vue.prototype.$http = axios
Vue.prototype.$url = "http://127.0.0.1:8000/"
Vue.prototype.$API = API
Vue.prototype.$get = fetch.get
Vue.prototype.$post = fetch.post
Vue.prototype.$put = fetch.put
Vue.prototype.$del = fetch.delete
Vue.prototype.$qs = qs

new Vue({
  axios,
  router,
  render: h => h(App),
}).$mount('#app')

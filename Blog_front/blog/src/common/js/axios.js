import axios from "axios";

// 构建axios实例
const instance = axios.create({
	baseURL: '/',  // 该处url会根据开发环境进行变化（开发/发布）
	timeout: 10000  // 设置请求超时连接时间
})


export default {
  install: (Vue) => {
    Object.defineProperty(Vue.prototype, '$axios', { value: instance })
  }
}
  
import axios from 'axios'
import element from 'element-ui'
// import qs from 'qs'

// respone拦截器
axios.interceptors.response.use(response => {
    return response.data
  }, error => {
    return error.data
})
axios.defaults.withCredentials = true


function timestampToTime(){
    let date = new Date(),
      Y = date.getFullYear() + '-',
      M = (date.getMonth() + 1 < 10 ? '0' + (date.getMonth() + 1) : date.getMonth() + 1) + '-',
      D = date.getDate() + ' ',
      h = date.getHours() + ':',
      m = date.getMinutes() + ':',
      s = date.getSeconds()
    return Y + M + D + h + m + s
}
  
export default {
    post(url, data) {
      return axios({
        method: 'post',
        url,
        // changeOrigin:true,
        // data: qs.stringify(data),
        data:JSON.stringify(data),
        timeout: 15000,
        dataType:"json",
        headers: {
           'content-type':' application/json',
        }
      }).then(
        (response) => {
          if(response.status == "301") {
            element.Message({
              message: response.msg,
              type: 'error'
            })
            return ;
          }
          return response
        }
      ).then(
        (res) => {
          return res
        }
      )
    },
  
    upload(url, data) {
      let form = new FormData()
      Object.keys(data).forEach(value => {
        form.append(value, data[value])
      })
      return axios({
        method: 'post',
        // baseURL: process.env.BASE_API,
        url,
        data,
        transformRequest: [function (data) {
          let ret = ''
          for (let it in data) {
            ret += encodeURIComponent(it) + '=' + encodeURIComponent(data[it]) + '&'
          }
          return ret
        }],
        timeout: 15000,
        headers: {
          // 'X-Requested-With': 'XMLHttpRequest',
          // 'Access-Control-Allow-Origin': '*',
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      }).then(
        (response) => {
          return response
        }
      ).then(
        (res) => {
          return res
        }
      )
    },
  
    get(url, params) {
  
      return axios({
        method: 'get',
        headers:{
          "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
          'Accept': 'application/json',
        },
        // baseURL: process.env.BASE_API,
        url,
        params, // get 请求时带的参数
        timeout: 15000
      }).then(
        (response) => {
          return response
        }
      ).then(
        (res) => {
          return res
        }
      )
    },
    delete(url, params) {
      return axios({
        method: 'delete',
        url,
        data:JSON.stringify(params), // get 请求时带的参数
        dataType:'json',
        headers:{
          'content-type':' application/json',
        },
  
        // baseURL: process.env.BASE_API,
  
        timeout: 15000
      }).then(
          (response) => {
            return response
          }
      ).then(
          (res) => {
            return res
          }
      )
    },
    put(url, data) {
      return axios({
        method: 'put',
        headers:{
          "Content-Type": "application/x-www-form-urlencoded",
        },
        dataType: "json",
        processData: false,  // 不处理数据
        contentType: false,
        // baseURL: process.env.BASE_API,
        url,
        data,
        timeout: 15000
      }).then(
        (response) => {
          return response
        }
      ).then(
        (res) => {
          return res
        }
      )
    },
    time(tamp) {
      return timestampToTime(tamp)
    }
}
  
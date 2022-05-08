const serverBase = 'http://localhost:8000/'
export default {
  // 基础接口
  BASE_SERVER_URL: serverBase,
  // 登录
  API_LOGIN: serverBase + 'user/login/',
  // 获取验证码
  API_GET_CODE: serverBase + 'user/code/',
  // 获取分类
  API_GET_CATEGORY: serverBase + 'blog/getCategory/',
  // 获取标签
  API_GET_LABEL: serverBase + 'blog/getLabel/',
  // 上传图片
  API_UPLOAD_IMG: serverBase + 'blog/uploadImg/',
  // 发布博客
  API_PUT_POST: serverBase + 'blog/publish/',
  // 获取博客列表
  API_GET_POSTS: serverBase + 'blog/postList/',
  // 获取博客内容/更新博客阅读量
  API_POST: serverBase + 'blog/post/',
  // 点赞
  API_LIKE: serverBase + 'user/like/',
  // 根据标签获得博客
  API_GET_POST_BY_LABEL: serverBase + 'blog/byLabel/',
  // 根据分类获得博客
  API_GET_POST_BY_CATEGORY: serverBase + 'blog/byCategory/',
  // 获取/上传/更新/删除图集
  API_PICTURE: serverBase + 'picture/',
  // 获取图片详情
  API_GET_PICTURE_DESC: serverBase + 'picture/describe/',
  // 获取推荐图集
  API_GET_PICTURE_RECOMMEND: serverBase + 'picture/recommend/',
  // 获取数量
  API_GET_COUNT: serverBase + 'blog/count/',
  // 获取图片
  API_GET_IMG: serverBase + 'blog/getImg/',
  // 图集图片删除和添加
  API_UPDATE_PICUTRE: serverBase + 'picture/update/',
  // 博客搜索
  API_SEARCH_POSTS: serverBase + 'blog/search/',
  // 判断是否为站长
  API_IS_ADMIN: serverBase + 'user/admin/',
  // 获取用户信息/更新用户信息
  API_USER_INFO: serverBase + 'user/info/',
  // 用户评论
  API_USER_COMMENT: serverBase + 'user/comment/',
  // 获得博客评论
  API_POST_COMMENT: serverBase + 'blog/comment/',
  // 头像更新
  API_AVATAR: serverBase + 'user/avatar/',
  // 登录
  API_REGISTER: serverBase + 'user/register/',
  // 热门
  API_HOT: serverBase + 'blog/hot/',

}
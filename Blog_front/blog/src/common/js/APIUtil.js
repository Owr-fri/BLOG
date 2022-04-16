const serverBase = 'http://localhost:8000/'
export default{
    // 基础接口
    BASE_SERVER_URL: serverBase,
    // 登录
    API_LOGIN: serverBase + 'login/',
    // 获取验证码
    API_GET_CODE : serverBase + 'getCode/',
    // 获取分类
    API_GET_CATEGORY: serverBase + 'getCategory/',
    // 获取标签
    API_GET_LABEL: serverBase + 'getLabel/',
    // 上传图片
    API_UPLOAD_IMG: serverBase + 'api/uploadImg/',
    // 发布博客
    API_PUT_POST: serverBase + 'api/publish/',
    // 获取博客列表
    API_GET_POSTS: serverBase + 'getPosts/',
    // 获取博客内容
    API_GET_POST: serverBase + 'getPost/',
    // 点赞
    API_LIKE: serverBase + 'like/',
    // 根据标签获得博客
    API_GET_POST_BY_LABEL: serverBase + 'getPostByLabel/',
    // 根据分类获得博客
    API_GET_POST_BY_CATEGORY: serverBase + 'getPostByCategory/'

}
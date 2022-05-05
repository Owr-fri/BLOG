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
    API_GET_POST_BY_CATEGORY: serverBase + 'getPostByCategory/',
    // 获取图集
    API_GET_PICTURES: serverBase + 'getPicture/',
    // 上传图集
    API_UPLOAD_PICTURE: serverBase + 'uploadPicture/',
    // 获取图片详情
    API_GET_PICTURE_DESC: serverBase + 'getPictureDesc/',
    // 获取推荐图集
    API_GET_PICTURE_RECOMMEND: serverBase + 'getPictureRec/',
    // 获取数量
    API_GET_COUNT: serverBase + 'getCount/',
    // 获取图片
    API_GET_IMG: serverBase + 'getImg/',
    // 图集图片删除和添加
    API_UPDATE_PICUTRE: serverBase + 'updatePicture/',
    // 博客搜索
    API_SEARCH_POSTS: serverBase + 'search/'
    

}
import json
import datetime
import os
import random
import shutil

from django.core.paginator import InvalidPage
from django.http import HttpResponse
from rest_framework.pagination import PageNumberPagination

from Blog import settings

# 返回状态码及信息
status_code = {
    200: '操作成功',
    201: '对象创建成功',
    202: '请求已经被接受',
    204: '操作已经执行成功，但是没有返回数据',
    301: '资源已被移除',
    303: '重定向',
    304: '资源没有被修改',
    400: '参数列表错误（缺少，格式不匹配)',
    401: '未授权',
    403: '访问受限，授权过期',
    404: '资源，服务未找到',
    405: '不允许的http方法',
    409: '资源冲突，或者资源被锁',
    415: '不支持的数据，媒体类型',
    500: '系统内部错误',
    501: '接口未实现'
}


# json 工具类
class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, datetime.time):
            return obj.strftime('%H:%M:%S')
        return json.JSONEncoder.default(self, obj)


# 查询成功
def response_success(code=None, message=None, data=None):
    if not message:
        message = status_code.get(code)
    return HttpResponse(json.dumps({
        'code': code,  # code由前后端配合指定
        'msg': message,  # 提示信息
        'data': data,  # 返回数据
        # 'count': len(data )# 总条数
    }, cls=JSONEncoder), 'application/json')


# 查询失败
def response_failure(code=None, message=None):
    if not message:
        message = status_code.get(code)
    return HttpResponse(json.dumps({
        'code': code,
        'msg': message
    }), 'application/json')


# 上传图片
def upload_image(img_file, upload_path):
    # 获取后缀名
    ext = img_file.name.split('.')[-1]
    # 如果上传图片的后缀名不在配置的后缀名里返回格式不允许
    if ext not in settings.ALLOWED_IMG_TYPE:
        return response_failure(code=415)
    # 新的文件名
    new_file_name = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + str(
        random.randint(10000, 99999)) + '.' + ext  # 采用时间和随机数
    path = upload_path + new_file_name
    with open(path, 'wb') as f:  # 二进制写入
        for i in img_file.chunks():
            f.write(i)
    return path


# 字典切片
def dict_slice(adict, start, end):
    keys = adict.keys()
    dict_slice = {}
    for k in list(keys)[start:end]:
        dict_slice[k] = adict[k]
    return dict_slice


# 删除文件夹
def del_dict(rootdir):
    filelist = os.listdir(rootdir)
    for f in filelist:
        filepath = os.path.join(rootdir, f)
        if os.path.isfile(filepath):
            os.remove(filepath)
        elif os.path.isdir(filepath):
            shutil.rmtree(filepath, True)
    # os.remove(rootdir)


# 验证登录
def check_login(func):
    def wrapper(request, *args, **kwargs):
        session_get_userId = request.session.get('id')
        if session_get_userId:
            if request.method == 'GET':
                userId = request.GET.get('id') if request.GET.get('id') else request.GET.get('userId')
            else:
                userId = request.data.get('id') if request.data.get('id') else request.data.get('userId')
            print(f"session-get-id:{session_get_userId},user-id:{userId}")
            if str(session_get_userId) != str(userId):
                return response_failure(401, message='请重新登录')
            return func(request, *args, **kwargs)
        return response_failure(401, message='登录已过期,请重新登录')
    return wrapper

# 验证是否为管理员
def check_admin(func):
    def wrapper(request, *args, **kwargs):
        session_get_role = request.session.get('role')
        if session_get_role == 's':
            return func(request, *args, **kwargs)
        return response_failure(401, message='授权失败，请重新登录')
    return wrapper
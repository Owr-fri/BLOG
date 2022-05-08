import redis
import smtplib
import hashlib
import numpy as np
from email.mime.text import MIMEText
from email.header import Header
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from Blog.settings import EMAIL_FROM, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, EMAIL_HOST, EMAIL_PORT, subject
from Blog.Utils.utils import *
from Blog.Utils.serializers import *


r = redis.Redis(host='localhost', port=6379, decode_responses=True)


class Login(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("pwd")
        verify = request.data.get("verify")
        time = request.data.get("time").replace('/', '-')
        # 加密
        pwd_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
        # 校验邮箱验证码
        code = r.get(username + "_code")
        if verify == code:
            user_obj = Users.objects.filter(email=username).first()
            user_pwd = user_obj.pwd
            if user_pwd == pwd_hash:
                # 删除code
                r.delete(username + "_code")
                user_obj.loginTime = time
                request.session['is_login'] = 'true'  # 是否已经登录
                request.session['id'] = user_obj.id  # 登录用户id
                request.session['role'] = user_obj.role  # 用户角色
                user_obj.save()
                request.session.save()
                return response_success(code=200,
                                        data={"id": user_obj.id, "avatar": str(user_obj.avatar), "name": user_obj.name,
                                              "role": user_obj.role})
        return response_failure(202, message="登录失败")

    # 退出
    @method_decorator(check_login)
    def get(self, request):
        request.session.clear()
        return response_success(200, message='成功退出')


class Code(APIView):
    def get(self, request):
        email = request.GET.get('email')
        code = "".join(str(i) for i in np.random.randint(0, 9, 4))
        html_content = """<div><p>您好,您的验证码为:%s</p></div>""" % code

        message = MIMEText(html_content, 'html', 'utf-8')
        message['From'] = Header(EMAIL_FROM, 'utf-8')
        message['To'] = Header(email, 'utf-8')
        message['message'] = Header(subject, 'utf-8')
        message['Subject'] = Header(subject, 'utf-8')

        try:
            server = smtplib.SMTP_SSL(EMAIL_HOST, EMAIL_PORT)
            server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
            server.sendmail(EMAIL_HOST_USER, [email], message.as_string())
            server.quit()
            r.set(email + "_code", code)
        except Exception:
            return Response(data="邮件发送失败")
        return Response(data="邮件发送成功")


class Like(APIView):
    @method_decorator(check_login)
    def post(self, request):
        data = request.data
        data['postId'] = Posts.objects.filter(id=data['postId']).first().id
        data['userId'] = Users.objects.filter(id=data['userId']).first().id
        serializer = LikeSerializers(data=data)
        if not serializer.is_valid():
            print(serializer.errors)
            return response_failure(304)
        serializer.save()
        return response_success(200)

    @method_decorator(check_login)
    def delete(self, request):
        postId = request.data.get("postId")
        userId = request.data.get("userId")
        id = request.data.get('likeId')
        flag, count = Likes.objects.filter(id=id).delete() if id else Likes.objects.filter(postId=postId,
                                                                                           userId=userId).delete()
        if flag:
            return response_success(200, message='删除成功')
        else:
            return response_failure(304, message='删除失败')

    @method_decorator(check_login)
    def get(self, request):
        userId = request.GET.get('id')
        objs = Likes.objects.filter(userId=userId).order_by('-id')
        res = []
        for obj in objs:
            data = LikeSerializers(obj).data
            data['title'] = Posts.objects.filter(id=data['postId']).first().title
            res.append(data)
        return response_success(200, data=res)


class Admin(APIView):
    def get(self, request):
        role = request.session.get("role")
        if role == "s":
            return response_success(200)
        elif role:
            return response_success(303, message="当前用户非管理员")
        else:
            return response_success(303, message="请先登录!")


class Info(APIView):
    @method_decorator(check_login)
    def get(self, request):
        id = request.GET.get('id')
        obj = Users.objects.filter(id=id).first()
        serializer = UserSerializers(obj)
        data = serializer.data
        res = {
            "name": data['name'],
            "email": data['email'],
            "avatar": str(data["avatar"])[1:] if str(data["avatar"]).startswith('/') else str(data["avatar"]),
            "role": data['role'],
            "loginTime": data["loginTime"],
            "phone": data['phone'] if data['phone'] else '暂无',
        }
        return response_success(200, data=res)

    @method_decorator(check_login)
    def put(self, request):
        id = request.data.get("id")
        name = request.data.get("name")
        phone = request.data.get("phone")
        avatar = request.data.get('avatar')
        flag = Users.objects.filter(id=id).update(name=name, phone=phone, avatar=avatar)
        if flag:
            return response_success(200, message="用户信息修改成功")
        else:
            return response_failure(304, message="用户信息修改失败")


class Comment(APIView):
    @method_decorator(check_login)
    def post(self, request):
        data = request.data
        data["postId"] = Posts.objects.filter(id=data["postId"]).first().id
        data["userId"] = Users.objects.filter(id=data["userId"]).first().id
        data["time"] = data["time"].replace('/', '-')
        serializer = CommentSerializers(data=data)
        if not serializer.is_valid():
            return response_failure(code=400, message="数据格式错误")
        serializer.save()
        return response_success(200, data=serializer.data)

    @method_decorator(check_login)
    def get(self, request):
        userId = request.GET.get('userId')
        print(userId)
        comments = Comments.objects.filter(userId=userId).order_by('-time')
        res = []
        for comment in comments:
            name = comment.userId.name
            avatar = str(comment.userId.avatar)
            serializer = CommentSerializers(comment)
            data = serializer.data
            data['name'] = name
            data['avatar'] = avatar
            data['title'] = comment.postId.title

            res.append(data)
        return response_success(200, data=res)

    @method_decorator(check_login)
    def delete(self, request):
        id = request.data.get('commentId')
        flag, count = Comments.objects.filter(id=id).delete()
        if flag:
            return response_success(200, message='删除成功')
        else:
            return response_success(202, message="删除失败")


class Avatar(APIView):
    def post(self, request):
        img = request.FILES.get("file")
        upload_path = upload_image(img, 'static/user/')
        return response_success(200, data={"avatar": upload_path})


class Register(APIView):
    def post(self, request):
        data = request.data
        if data['comfirm'] == data['pwd']:
            data['pwd'] = hashlib.sha256(data['pwd'].encode('utf-8')).hexdigest()
            del data['comfirm']
            serializer = UserSerializers(data=data)
            if serializer.is_valid():
                serializer.save()
                return response_success(200, message='注册成功')
            return response_failure(304, message=serializer.errors)
        return response_failure(400, message="两次输入的密码不一致")

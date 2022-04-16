import json
import base64
import os
import shutil
import redis
import urllib.parse
import smtplib
import hashlib
import numpy as np
from email.mime.text import MIMEText
from email.header import Header
from django.views import View
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from Blog.settings import EMAIL_FROM, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, EMAIL_HOST, EMAIL_PORT, subject
from .models import *
from ..Utils.utils import *
from ..Utils.serializers import *

# Create your views here.
# 初始化redis对象
r = redis.Redis(host='localhost', port=6379, decode_responses=True)


class Login(APIView):
    def post(self, request):
        data = request.data.get('data')
        email, pwd, verify = data.split("&")
        email = urllib.parse.unquote(email.split("=")[1])
        pwd = pwd.split("=")[1]
        verify = verify.split("=")[1]
        # 加密
        pwd_hash = hashlib.sha256(pwd.encode('utf-8')).hexdigest()
        # 校验邮箱验证码
        code = r.get(email + "_code")
        if verify == code:
            user_obj = Users.objects.filter(email=email).first()
            user_pwd = user_obj.pwd
            if user_pwd == pwd_hash:
                # 删除code
                # r.delete(email + "_code")
                return response_success(code=200, data='登录成功')
        return Response(data="登录失败")


class GetCode(APIView):
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


def getCategory(request):
    obj = Categorys.objects.values()
    serializers = CategorySerializers(obj, many=True)
    res = []
    try:
        data = serializers.data
        for item in data:
            res.append({"id": item["id"],
                        "category": item["categoryName"]})
        return response_success(code=200, data=res)
    except:
        return response_failure(code=500)


def getLabel(request):
    obj = Labels.objects.values()
    serializers = LabelSerializers(obj, many=True)
    res = []
    try:
        data = serializers.data
        for item in data:
            res.append({"id": item["id"],
                        "label": item["labelName"]})
        return response_success(code=200, data=res)
    except:
        return response_failure(code=500)


def uploadImg(request):
    i = 1
    imgPath = request.FILES.getlist("Image")
    print(imgPath)
    folder = "static/temp/"

    upload_path = upload_image(*imgPath, folder)
    res = {
        "errno": 0,
        "data": {"url": "http://" + request.get_host() + '/' + upload_path}
    }
    return HttpResponse(json.dumps(res))


class Publish(APIView):
    def post(self, request):
        data = request.data
        imgList1 = [i['src'].split('/')[-1] for i in data["imgList"]]
        # print(data)
        # 修改数据，让其符合serializer的校验
        data = dict_slice(data, 0, -1)
        data["content"] = data["content"].replace("static/temp/", "static/upload/")

        # 判断是否要添加分类和标签
        if str(data["categoryId"]).isdigit():
            data["categoryId"] = Categorys.objects.filter(id=data["categoryId"]).first().id
        else:
            data["categoryId"] = Categorys.objects.create(categoryName=data["categoryId"]).id

        labelId = []
        for label in data["labelId"].split(','):
            if str(label).isdigit():
                labelId.append(Labels.objects.filter(id=label).first().id)
            else:
                labelId.append(Labels.objects.create(labelName=label).id)
        data["labelId"] = labelId

        # 序列化操作
        serializer = PostSerializers(data=data)
        if not serializer.is_valid():
            return response_failure(code=400, message="数据格式错误")

        instance = serializer.save()
        try:
            if instance and imgList1:  # 判断是否保存为空再删除temp多余的图
                imgList2 = os.listdir("static/temp/")
                for img in imgList2:
                    if img in imgList1:
                        shutil.move("static/temp/" + img, "static/upload/")
                    else:
                        os.remove("static/temp/" + img)
            return response_success(code=200, message="发布成功")
        except:
            return response_failure(code=500, message="发布失败，请稍后发布")


class GetPosts(APIView):
    def get(self, request):
        # 排序
        queryset = Posts.objects.all().order_by("-id")
        # 总数
        if queryset:
            total = queryset.count()
            serializer = PostSerializers
            # 分页
            page = PageNumberPagination()
            course_list = page.paginate_queryset(queryset, request, self)
            # 分页之后序列化
            ser = serializer(instance=course_list, many=True)
            posts = []
            for data in ser.data:
                posts.append({
                    "id": data["id"],
                    "title": data["title"],
                    "summary": data["summary"],
                    "author": data["author"],
                    "publishTime": data["publishTime"],
                    "read_counts": data["read_counts"],
                    "comment_counts": data["comment_counts"],
                    "like_counts": data["like_counts"],
                    "categoryName": data["categoryName"],
                    "categoryId":data["categoryId"]
                })
            res = {
                "posts": posts,
                "total": total,
            }
            return response_success(code=200, data=res)
        return response_failure(code=404, message="分页请求失败")


class GetPost(APIView):
    def get(self, request):
        postId = request.GET.get("id", "")
        obj = Posts.objects.filter(id=postId)
        prev_obj = Posts.objects.filter(id__lt=postId).all().order_by("-id").first()
        next_obj = Posts.objects.filter(id__gt=postId).all().order_by("id").first()
        if obj:
            serializer = PostSerializers(obj, many=True)

            data = serializer.data[0]
            res = {
                "id": data["id"],
                "title": data["title"],
                "content": data["content"],
                "author": data["author"],
                "publishTime": data["publishTime"],
                "like_counts": data["like_counts"],
                "read_counts": data["read_counts"],
                "comment_counts": data["comment_counts"],
                "category": {
                    "id": data['categoryId'],
                    "name": data["categoryName"]
                },
                "label": [{"id": i[0], "name": i[1]} for i in [i for i in zip(data["labelId"], data["labelName"])]],
                "next": {
                    "id": next_obj.id if next_obj else -1,
                    "title": next_obj.title if next_obj else '没有下一条啦',
                },
                "prev": {
                    "id": prev_obj.id if prev_obj else -1,
                    "title": prev_obj.title if prev_obj else '没有上一条啦',
                }
            }
            return response_success(code=200, data=res)
        return response_failure(code=404, message="博客请求失败")


class Like(APIView):
    def post(self, request):
        postId = request.data.get('id', '')
        counts = request.data.get('counts', '')
        post = Posts.objects.filter(id=postId).update(like_counts=counts)

        return response_failure(501)


class GetPostByLabel(APIView):
    def get(self, request):
        id = request.GET.get('id', '')
        obj = Posts.objects.filter(labelId=id)
        res = []

        serializer = PostSerializers(obj, many=True)
        for data in serializer.data:
            res.append({
                "id": data["id"],
                "title": data["title"],
                "author": data["author"],
                "time": data["publishTime"],
                "like_counts": data["like_counts"],
                "read_counts": data["read_counts"],
                "comment_counts": data["comment_counts"],
            })
        return response_success(code=200, data=res)


class GetPostByCategory(APIView):
    def get(self, request):
        id = request.GET.get('id', '')
        obj = Posts.objects.filter(categoryId=id)
        res = []

        serializer = PostSerializers(obj, many=True)
        for data in serializer.data:
            res.append({
                "id": data["id"],
                "title": data["title"],
                "author": data["author"],
                "time": data["publishTime"],
                "like_counts": data["like_counts"],
                "read_counts": data["read_counts"],
                "comment_counts": data["comment_counts"],
            })
        return response_success(code=200, data=res)
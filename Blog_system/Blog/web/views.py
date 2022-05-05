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
from django.http import QueryDict
from django.db.models import Count, Min, Max, Sum
from django.db.models import QuerySet
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
                        "name": item["categoryName"]})
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
                        "name": item["labelName"]})
        return response_success(code=200, data=res)
    except:
        return response_failure(code=500)


class uploadImg(APIView):
    def post(self, request):
        img = request.FILES.get("img")
        upload_path = upload_image(img, 'static/upload/blog/')
        return response_success(200, data={"url": upload_path})

    def delete(self, request):
        img = request.data.get('img')
        path = 'static' + img.split("static")[1]
        os.remove(path)
        return response_success(200, message="删除成功")


class Publish(APIView):
    def post(self, request):
        data = request.data

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
        if instance:  # 判断是否保存为空再删除temp多余的图
            return response_success(code=200, message="发布成功")
        else:
            return response_failure(code=500, message="发布失败，请稍后发布")

    def put(self, request):
        data = request.data.dict()
        id = data['id']
        try:
            obj = Posts.objects.filter(id=id).first()
            serializer = PostSerializers()
            serializer.update(obj, data)
            return response_success(200)
        except:
            return response_failure(304, message="保存失败")

    def delete(self, request):
        id = request.data['id']
        Posts.objects.filter(id=id).update(isDel=True)
        return response_success(200, message='删除成功')


class GetPosts(APIView):
    def get(self, request):
        # 排序
        queryset = Posts.objects.exclude(isDel=True).order_by("-id")
        # status: -1为分页获取，1为获取全部，2为获取搜索列表
        status = request.GET.get('status', '-1')
        # 总数
        if queryset:
            total = queryset.count()
            serializer = PostSerializers
            if status == '-1':
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
                        "categoryId": data["categoryId"],
                        "labelName": data["labelName"],
                        "labelId": data["labelId"],
                    })
                res = {
                    "posts": posts,
                    "total": total,
                }
                return response_success(code=200, data=res)

            if status == '1':
                ser = serializer(instance=queryset, many=True)
                return response_success(code=200, data=ser.data)

            if status == '2':
                ser = serializer(instance=queryset, many=True)
                res = []
                for data in ser.data:
                    res.append({
                        "value": data["title"],
                        "id": data["id"],
                    })
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
        Posts.objects.filter(id=postId).update(like_counts=counts)

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


class GetPicture(APIView):
    def get(self, request):
        obj = Pictures.objects.filter(sort=1).order_by('id')
        serializer = PictureSerializers(obj, many=True)
        res = []
        for data in serializer.data:
            res.append({
                "img": "http://" + request.get_host() + data["imgPath"],
                "title": data["title"],
                "summary": data["summary"],
            })

        return response_success(code=200, data=res)


class PublishPicture(APIView):
    def post(self, request):
        images = request.FILES.getlist("file")
        summary = request.data.get('summary')
        # 创建文件夹
        title = datetime.datetime.now().strftime("%Y年%m月%d日%H时%M分%S秒")
        pic_dic = os.path.join('static\\picture', title + '\\')
        os.mkdir(pic_dic)

        i = 1
        if images:
            for image in images:
                print(image)
                upload_path = upload_image(image, pic_dic)
                Pictures.objects.create(imgPath=upload_path, title=title, summary=summary,sort=i)
                i += 1
            return response_success(code=200, message="图集上传成功")

    def put(self,request):
        summary = request.data.get("summary")
        idList = request.data.get("imglist").split(",")
        i = 1
        if idList:
            for id in idList:
                Pictures.objects.filter(id=id).update(sort=i,summary=summary)
                i += 1
            return response_success(code=200,message="更新成功")
        return response_failure(304,message="更新失败")

    def delete(self,request):
        title = request.data.get("title")
        try:
            Pictures.objects.filter(title=title).delete()
            del_dict("static/picture/"+title)
            return response_failure(200,message="删除成功")
        except:
            return response_failure(409,message="删除失败")


class GetPictureDesc(APIView):
    def get(self, request):
        title = request.GET.get("title", '')
        obj = Pictures.objects.filter(title=title).order_by("sort")
        prev_obj = Pictures.objects.filter(id__lt=obj.first().id, sort=1).all().order_by("-id").first()
        next_obj = Pictures.objects.filter(id__gt=obj.first().id, sort=1).all().order_by("id").first()
        res = []
        if obj:
            serializer = PictureSerializers(obj, many=True)
            for data in serializer.data:
                res.append({
                    "id": data["id"],
                    "img": data["imgPath"][1:],
                })
            summary = serializer.data[0]["summary"]
            prev = {
                "id": prev_obj.id if prev_obj else -1,
                "title": prev_obj.title if prev_obj else '没有上一条啦',
            }
            next = {
                "id": next_obj.id if next_obj else -1,
                "title": next_obj.title if next_obj else '没有下一条啦',
            }

            return response_success(200, data={"title": title, "imglist": res, "summary": summary,
                                               "prev": prev, "next": next})
        return response_failure(404, message="图集请求失败")


class GetPictureRec(APIView):
    def get(self, request):
        title = request.GET.get("title", '')
        obj = Pictures.objects.exclude(title=title).filter(sort=1)[:6]
        res = []
        if obj:
            serializer = PictureSerializers(obj, many=True)
            for data in serializer.data:
                res.append({
                    "id": data["id"],
                    "img": data["imgPath"][1:],
                    "title": data["title"],
                })
            random.shuffle(res)
            return response_success(200, data=res)
        return response_failure(501)


class GetCount(APIView):
    def get(self, request):
        post = Posts.objects.all().count()
        label = Labels.objects.all().count()
        picture = Pictures.objects.filter(sort=1).count()
        return response_success(200, data={
            "post": post,
            "label": label,
            "picture": picture,
        })


class GetImg(APIView):
    def get(self, request):
        path = request.GET.get("img")
        img_byte = open('static' + path, 'rb').read()
        return HttpResponse(img_byte)


class UpdatePicutre(APIView):
    def put(self, request):
        title = request.data.get('title')
        file = request.data.get('file')
        summary = request.data.get('summary')
        pic_dic = os.path.join('static\\picture', title + '\\')
        upload_path = upload_image(file, pic_dic)
        count = Pictures.objects.filter(title=title).count() + 1
        obj = Pictures.objects.create(imgPath=upload_path, title=title, summary=summary,sort=count)
        return response_success(code=200, data={"id": obj.id, "img": str(obj.imgPath)})

    def delete(self,request):
        id = request.data.get('id')
        obj = Pictures.objects.filter(id=id).first()
        path = str(obj.imgPath)
        obj.delete()
        os.remove(path)
        return response_failure(200,message="删除成功")


class Search(APIView):
    def get(self,request):
        key = request.GET.get('key')
        queryset = Posts.objects.filter(title__contains=key).order_by("id")
        total = queryset.count()
        page = PageNumberPagination()
        course_list = page.paginate_queryset(queryset, request, self)
        # 分页之后序列化
        serializer = PostSerializers
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
                "categoryId": data["categoryId"],
            })
        res = {
            "posts": posts,
            "total": total,
        }

        return response_success(code=200, data=res)

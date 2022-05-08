from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from Blog.Utils.utils import *
from Blog.Utils.serializers import *


# Create your views here.
# 初始化redis对象

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
    @method_decorator(check_admin)
    def post(self, request):
        print(request.FILES)
        img = request.FILES.get("img")
        upload_path = upload_image(img, 'static/upload/blog/')
        return response_success(200, data={"url": upload_path})

    @method_decorator(check_admin)
    def delete(self, request):
        img = request.data.get('img')
        path = 'static' + img.split("static")[1]
        os.remove(path)
        return response_success(200, message="删除成功")


class Publish(APIView):
    @method_decorator(check_admin)
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

    @method_decorator(check_admin)
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

    @method_decorator(check_admin)
    def delete(self, request):
        id = request.data['id']
        Posts.objects.filter(id=id).update(isDel=True)
        return response_success(200, message='删除成功')


class PostList(APIView):
    def get(self, request):
        # 排序
        queryset = Posts.objects.exclude(isDel=True).order_by("-id")
        # status: -1为分页获取，1为获取全部，2为获取搜索列表
        status = request.GET.get('status', '-1')
        # 总数
        if queryset:
            total = queryset.count()
            print(status,len(queryset))
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


class Post(APIView):
    @method_decorator(check_admin)
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

    def get(self, request):
        postId = request.GET.get("id", "")
        userId = request.GET.get('userId', '')
        obj = Posts.objects.filter(id=postId)
        like_counts = Likes.objects.filter(postId=postId).count()
        comment_counts = Comments.objects.filter(postId=postId).count()
        prev_obj = Posts.objects.filter(id__lt=postId).all().order_by("-id").first()
        next_obj = Posts.objects.filter(id__gt=postId).all().order_by("id").first()
        isLike = 0
        if userId:
            isLike = Likes.objects.filter(postId=postId, userId=userId).count()
        if obj:
            serializer = PostSerializers(obj, many=True)

            data = serializer.data[0]
            res = {
                "id": data["id"],
                "title": data["title"],
                "content": data["content"],
                "author": data["author"],
                "publishTime": data["publishTime"],
                "like_counts": like_counts,
                "read_counts": data["read_counts"],
                "comment_counts": comment_counts,
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
                },
                "islike": isLike
            }
            return response_success(code=200, data=res)
        return response_failure(code=404, message="博客请求失败")

    @method_decorator(check_login)
    def put(self, request):
        postId = request.data.get('postId')
        read_counts = request.data.get('read_counts')
        print(postId, read_counts)
        flag = Posts.objects.filter(id=postId).update(read_counts=read_counts)
        if flag:
            return response_success(200, message='阅读量加一')
        else:
            return response_failure(304)


class ByLabel(APIView):
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


class ByCategory(APIView):
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


class Count(APIView):
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


class Search(APIView):
    def get(self, request):
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


class Comment(APIView):
    def get(self, request):
        postId = request.GET.get('postId')
        comments = Comments.objects.filter(postId=postId).order_by('time')
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


class Hot(APIView):
    def get(self, request):
        res = []
        objs = Posts.objects.exclude(isDel=1).order_by("likes", 'comments', 'read_counts')
        serializer = PostSerializers(objs,many=True)
        data = serializer.data if len(serializer.data)<3 else serializer.data[:3]
        for d in data:
            res.append({
                "id":d["id"],
                "title":d["title"],
                "summary":d["summary"],
                "author":d["author"]
            })

        return response_success(200,data=serializer.data)

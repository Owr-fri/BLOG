
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from ..Utils.utils import *
from ..Utils.serializers import *
# Create your views here.


class Picture(APIView):
    # 获取
    def get(self, request):
        obj = Pictures.objects.filter(sort=1).order_by('title')
        serializer = PictureSerializers(obj, many=True)
        res = []
        for data in serializer.data:
            res.append({
                "img": str(data["imgPath"])[1:] if str(data["imgPath"]).startswith('/') else str(data["imgPath"]),
                "title": data["title"],
                "summary": data["summary"],
            })

        return response_success(code=200, data=res)

    # 发布图集
    @method_decorator(check_admin)
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
                Pictures.objects.create(imgPath=upload_path, title=title, summary=summary, sort=i)
                i += 1
            return response_success(code=200, message="图集上传成功")

    # 更新图集
    @method_decorator(check_admin)
    def put(self, request):
        summary = request.data.get("summary")
        idList = request.data.get("imglist").split(",")
        i = 1
        if idList:
            for id in idList:
                Pictures.objects.filter(id=id).update(sort=i, summary=summary)
                i += 1
            return response_success(code=200, message="更新成功")
        return response_failure(304, message="更新失败")

    # 删除图集
    @method_decorator(check_admin)
    def delete(self, request):
        title = request.data.get("title")
        # try:
        Pictures.objects.filter(title=title).delete()
        del_dict("static/picture/" + title)
        return response_failure(200, message="删除成功")
        # except:
        #     return response_failure(409, message="删除失败")

class Update(APIView):
    # 图集图片的添加
    @method_decorator(check_admin)
    def put(self, request):
        title = request.data.get('title')
        file = request.data.get('file')
        summary = request.data.get('summary')
        pic_dic = os.path.join('static\\picture', title + '\\')
        upload_path = upload_image(file, pic_dic)
        count = Pictures.objects.filter(title=title).count() + 1
        obj = Pictures.objects.create(imgPath=upload_path, title=title, summary=summary, sort=count)
        return response_success(code=200, data={"id": obj.id, "img": str(obj.imgPath)})

    # 图集图片的删除
    @method_decorator(check_admin)
    def delete(self, request):
        id = request.data.get('id')
        obj = Pictures.objects.filter(id=id).first()
        path = str(obj.imgPath)
        obj.delete()
        os.remove(path)
        return response_failure(200, message="删除成功")


class Describe(APIView):
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


class Recommend(APIView):
    def get(self, request):
        title = request.GET.get("title", '')
        obj = Pictures.objects.exclude(title=title).filter(sort=1)[:6]
        res = []
        if obj:
            serializer = PictureSerializers(obj, many=True)
            for data in serializer.data:
                res.append({
                    "id": data["id"],
                    "img": str(data["imgPath"])[1:] if str(data["imgPath"]).startswith('/') else str(data["imgPath"]),
                    "title": data["title"],
                })
            random.shuffle(res)
            return response_success(200, data=res)
        return response_failure(501)

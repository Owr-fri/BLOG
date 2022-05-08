from Blog.web.models import *
from rest_framework import serializers
import time


class UserSerializers(serializers.ModelSerializer):
    """ 用户序列表 """

    class Meta:
        model = Users
        fields = "__all__"


class CategorySerializers(serializers.ModelSerializer):
    """ 分类序列表 """

    # id = serializers.IntegerField()
    # CategoryName = serializers.CharField()

    class Meta:
        model = Categorys
        fields = "__all__"

    # 获取分类名
    def get_category(self, obj):
        category = obj
        categoryName = []
        items = category.objects.values()
        for item in items:
            categoryName.append(item["categoryName"])
        return categoryName


class LabelSerializers(serializers.ModelSerializer):
    """ 标签序列表 """

    class Meta:
        model = Labels
        fields = "__all__"


class PostSerializers(serializers.ModelSerializer):
    """ 博客序列表 """

    class Meta:
        model = Posts
        fields = "__all__"

        id = serializers.IntegerField(label='帖子ID', read_only=True)
        title = serializers.CharField(label='标题', max_length=50)
        summary = serializers.CharField(allow_null=True, label='简要', max_length=100)
        content = serializers.CharField(label='内容', max_length=15000)
        author = serializers.CharField(label='作者', max_length=20, required=False)
        publishTime = serializers.DateField(label='发布时间', read_only=True)
        read_counts = serializers.IntegerField(label='阅读数', max_value=2147483647, min_value=-2147483648, required=False)
        comment_counts = serializers.IntegerField(label='评论数', max_value=2147483647, min_value=-2147483648,
                                                  required=False)
        like_counts = serializers.IntegerField(label='喜欢数', max_value=2147483647, min_value=-2147483648, required=False)
        categoryId = serializers.PrimaryKeyRelatedField(label='分类ID', queryset=Categorys.objects.all(),required=False)
        labelId = serializers.PrimaryKeyRelatedField(label='标签ID', many=True, queryset=Labels.objects.all(),
                                                     required=False)

    def create(self, validated_data):
        instance = Posts.objects.create(title=validated_data["title"], summary=validated_data["summary"],
                                        content=validated_data["content"],
                                        categoryId_id=validated_data["categoryId"].id)
        instance.labelId.set(validated_data["labelId"])
        return instance

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['like_counts'] = Likes.objects.filter(postId=data['id']).count()
        data['comment_counts'] = Comments.objects.filter(postId=data['id']).count()
        data["categoryName"] = Categorys.objects.filter(id=data["categoryId"]).first().categoryName
        data["labelName"] = [Labels.objects.filter(id=i).first().labelName for i in data["labelId"]]
        return data

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.summary = validated_data.get('summary', instance.summary)
        instance.categoryId = Categorys.objects.filter(id=(validated_data.get('category', instance.categoryId))).first()
        instance.labelId.set(validated_data.get('label', instance.labelId).split(','))
        instance.save()
        return instance


class PictureSerializers(serializers.ModelSerializer):
    """ 图集序列表 """

    class Meta:
        model = Pictures
        fields = "__all__"

class CommentSerializers(serializers.ModelSerializer):
    """ 评论序列表 """

    class Meta:
        model = Comments
        fields = "__all__"

        id = serializers.IntegerField(label='评论ID', read_only=True)
        comment = serializers.CharField(label='评论内容', max_length=255)
        time = serializers.DateTimeField(label='评论时间')
        postId = serializers.PrimaryKeyRelatedField(label='帖子ID', queryset=Posts.objects.all())
        userId = serializers.PrimaryKeyRelatedField(label='用户ID', queryset=Users.objects.all())

    def create(self, validated_data):
        instance = Comments.objects.create(**validated_data)
        return instance

class LikeSerializers(serializers.ModelSerializer):
    """ 评论序列表 """

    class Meta:
        model = Likes
        fields = "__all__"


    def create(self, validated_data):
        instance = Likes.objects.create(**validated_data)
        return instance
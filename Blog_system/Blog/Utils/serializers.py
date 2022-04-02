from Blog.web.models import Users
from rest_framework import serializers
import time


class UserSerializers(serializers.ModelSerializer):
    """ 用户序列表 """

    class Meta:
        model = Users
        fields = "__all__"

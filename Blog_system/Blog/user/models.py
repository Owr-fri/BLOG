from django.db import models
from Blog.web.models import Posts

# Create your models here.
class Users(models.Model):
    class META:
        db_table = "user"
        verbose_name = u'用户表'

    id = models.AutoField(verbose_name=u"用户ID", primary_key=True)
    name = models.CharField(verbose_name=u"用户名", max_length=25, null=False)
    avatar = models.ImageField(upload_to='static/user', verbose_name=u"头像", default="static/user/avatar.jpg")
    email = models.EmailField(null=False, verbose_name=u"邮箱", unique=True)
    phone = models.CharField(verbose_name=u"电话", max_length=11, null=True)
    pwd = models.CharField(max_length=255, verbose_name=u"密码", null=False)
    loginTime = models.DateField(null=True)
    role = models.CharField(max_length=2, choices=((u"s", u"superuser"), (u"u", u"user"), (u"v", u"visitor")),
                            default=u"u")


class Likes(models.Model):
    class META:
        db_table = "likes"
        verbose_name = u"点赞表"

    id = models.AutoField(verbose_name=u'点赞ID', primary_key=True)
    postId = models.ForeignKey(verbose_name=u'帖子ID', to=Posts, on_delete=models.CASCADE)
    userId = models.ForeignKey(verbose_name=u'用户ID', to='Users', on_delete=models.CASCADE)


class Comments(models.Model):
    class META:
        db_table = "comments"
        verbose_name = u"评论表"

    id = models.AutoField(verbose_name=u'评论ID', primary_key=True)
    comment = models.CharField(verbose_name=u'评论内容', max_length=255)
    postId = models.ForeignKey(verbose_name=u'帖子ID', to=Posts, on_delete=models.CASCADE)
    userId = models.ForeignKey(verbose_name=u'用户ID', to='Users', on_delete=models.CASCADE)
    time = models.DateTimeField(verbose_name=u'评论时间')

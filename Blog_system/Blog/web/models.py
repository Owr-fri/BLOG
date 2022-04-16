from django.db import models


# Create your models here.
class Users(models.Model):
    class META:
        app_label = "web"
        db_table = "user"
        verbose_name = u'用户表'

    id = models.AutoField(verbose_name=u"用户ID", primary_key=True)
    name = models.CharField(verbose_name=u"用户名", max_length=25, null=False)
    avatar = models.ImageField(upload_to='static/user', verbose_name=u"头像", null=True)
    email = models.EmailField(null=False, verbose_name=u"邮箱")
    pwd = models.CharField(max_length=255, verbose_name=u"密码", null=False)

class Posts(models.Model):
    class META:
        app_label = 'web'
        db_table = "posts"
        verbose_name = u"用户表"

    id = models.AutoField(verbose_name=u'帖子ID',primary_key=True)
    title = models.CharField(verbose_name=u'标题',max_length=50,null=False)
    summary = models.CharField(verbose_name=u'简要',max_length=100,null=True)
    content = models.CharField(verbose_name=u'内容',max_length=15000,null=False)
    author = models.CharField(verbose_name=u'作者',default='Owr',max_length=20)
    publishTime = models.DateField(verbose_name=u'发布时间',auto_now_add=True)
    read_counts = models.IntegerField(verbose_name=u'阅读数',default=0)
    comment_counts = models.IntegerField(verbose_name=u'评论数',default=0)
    like_counts = models.IntegerField(verbose_name=u'喜欢数',default=0)
    # categoryId = models.IntegerField(verbose_name=u'分类ID',null=False)
    # labelId = models.IntegerField(verbose_name=u'标签ID',null=False)
    categoryId = models.ForeignKey(verbose_name=u'分类ID',to='Categorys',on_delete=models.CASCADE)
    # label = models.ForeignKey(verbose_name=u'标签ID',to='Labels',on_delete=models.CASCADE)
    labelId = models.ManyToManyField(verbose_name=u'标签ID', to='Labels',blank=True)



class Categorys(models.Model):
    class META:
        app_label = 'web'
        db_table = "categorys"
        verbose_name = u"分类表"

    id = models.AutoField(verbose_name=u'分类ID',primary_key=True)
    categoryName = models.CharField(verbose_name=u'分类名称',max_length=100)


class Labels(models.Model):
    class META:
        app_label = 'web'
        db_table = "labels"
        verbose_name = u"标签表"

    id = models.AutoField(verbose_name=u'标签ID',primary_key=True)
    labelName = models.CharField(verbose_name=u'标签名称',max_length=100)



class Likes(models.Model):
    class META:
        app_label = 'web'
        db_table = "likes"
        verbose_name = u"点赞表"

    id = models.AutoField(verbose_name=u'点赞ID', primary_key=True)
    postId = models.ForeignKey(verbose_name=u'帖子ID',to='Posts',on_delete=models.CASCADE)
    userId = models.ForeignKey(verbose_name=u'用户ID',to='Users',on_delete=models.CASCADE)


class Comments(models.Model):
    class META:
        app_label = 'web'
        db_table = "comments"
        verbose_name = u"评论表"

    id = models.AutoField(verbose_name=u'评论ID', primary_key=True)
    comment = models.CharField(verbose_name=u'评论内容',max_length=255)
    postId = models.ForeignKey(verbose_name=u'帖子ID', to='Posts', on_delete=models.CASCADE)
    userId = models.ForeignKey(verbose_name=u'用户ID', to='Users', on_delete=models.CASCADE)
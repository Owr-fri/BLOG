from django.db import models


# Create your models here.

class Posts(models.Model):
    class META:
        db_table = "posts"
        verbose_name = u"用户表"

    id = models.AutoField(primary_key=True, verbose_name=u'帖子ID')
    title = models.CharField(max_length=50, verbose_name=u'标题', null=False)
    summary = models.CharField(max_length=100, verbose_name=u'简要', null=True)
    content = models.CharField(max_length=15000, verbose_name=u'内容', null=False)
    author = models.CharField(default='Owr', verbose_name=u'作者', max_length=20)
    publishTime = models.DateField(auto_now_add=True, verbose_name=u'发布时间')
    read_counts = models.IntegerField(default=0, verbose_name=u'阅读数')
    categoryId = models.ForeignKey(to='Categorys', verbose_name=u"分类ID", on_delete=models.CASCADE)
    isDel = models.BooleanField(default=False, verbose_name=u'是否删除')
    labelId = models.ManyToManyField(to='Labels', verbose_name=u'标签ID', blank=True)


class Categorys(models.Model):
    class META:
        db_table = "categorys"
        verbose_name = u"分类表"

    id = models.AutoField(verbose_name=u'分类ID', primary_key=True)
    categoryName = models.CharField(verbose_name=u'分类名称', max_length=100)


class Labels(models.Model):
    class META:
        db_table = "labels"
        verbose_name = u"标签表"

    id = models.AutoField(verbose_name=u'标签ID', primary_key=True)
    labelName = models.CharField(verbose_name=u'标签名称', max_length=100)


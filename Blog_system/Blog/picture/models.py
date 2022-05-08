from django.db import models

# Create your models here.
class Pictures(models.Model):
    class META:
        db_table = "pictures"
        verbose_name = u"图集表"

    id = models.AutoField(verbose_name=u"图集ID", primary_key=True)
    imgPath = models.ImageField(verbose_name=u'图片', upload_to='static/picture', null=True)
    title = models.CharField(verbose_name=u'标题', max_length=100)
    summary = models.CharField(verbose_name=u'简要', max_length=255)
    sort = models.IntegerField(verbose_name=u'序号')
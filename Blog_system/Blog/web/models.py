from django.db import models


# Create your models here.
class Users(models.Model):
    class META:
        app_label = "web"
        db_table = "user"
        verbose_name = '用户表'

    id = models.AutoField(verbose_name=u"用户ID", primary_key=True)
    name = models.CharField(verbose_name=u"用户名", max_length=25, null=True)
    avatar = models.ImageField(upload_to='static/user', verbose_name=u"头像", null=True)
    email = models.EmailField(null=True, verbose_name=u"邮箱")
    pwd = models.CharField(max_length=255, verbose_name=u"密码", null=True)

# Generated by Django 3.2.9 on 2022-05-08 15:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categorys',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='分类ID')),
                ('categoryName', models.CharField(max_length=100, verbose_name='分类名称')),
            ],
        ),
        migrations.CreateModel(
            name='Labels',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='标签ID')),
                ('labelName', models.CharField(max_length=100, verbose_name='标签名称')),
            ],
        ),
        migrations.CreateModel(
            name='Posts',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='帖子ID')),
                ('title', models.CharField(max_length=50, verbose_name='标题')),
                ('summary', models.CharField(max_length=100, null=True, verbose_name='简要')),
                ('content', models.CharField(max_length=15000, verbose_name='内容')),
                ('author', models.CharField(default='Owr', max_length=20, verbose_name='作者')),
                ('publishTime', models.DateField(auto_now_add=True, verbose_name='发布时间')),
                ('read_counts', models.IntegerField(default=0, verbose_name='阅读数')),
                ('isDel', models.BooleanField(default=False, verbose_name='是否删除')),
                ('categoryId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.categorys', verbose_name='分类ID')),
                ('labelId', models.ManyToManyField(blank=True, to='web.Labels', verbose_name='标签ID')),
            ],
        ),
    ]

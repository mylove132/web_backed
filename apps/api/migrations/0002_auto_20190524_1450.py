# Generated by Django 2.2.1 on 2019-05-24 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='env',
            field=models.IntegerField(choices=[(1, 'dev'), (2, 'docker-dev'), (3, 'docker-hotfix'), (4, 'stress')], default=1, verbose_name='项目环境'),
        ),
        migrations.AlterField(
            model_name='project',
            name='type',
            field=models.IntegerField(choices=[(1, '教师空间'), (2, '学生pad'), (3, '教师pad'), (4, '商城'), (5, 'OKAY+')], default=1, verbose_name='项目类型'),
        ),
        migrations.AlterField(
            model_name='script',
            name='method',
            field=models.CharField(blank=True, max_length=30, verbose_name='dubbo接口方法名'),
        ),
        migrations.AlterField(
            model_name='script',
            name='param_type',
            field=models.CharField(blank=True, default=1, max_length=100, verbose_name='dubbo接口请求参数类型'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='script',
            name='protocol',
            field=models.IntegerField(choices=[(1, 'GET'), (2, 'POST'), (3, 'DELETE')], default=1, verbose_name='接口协议'),
        ),
        migrations.AlterField(
            model_name='script',
            name='request_type',
            field=models.IntegerField(choices=[(1, 'GET'), (2, 'POST'), (3, 'DELETE')], default=1, verbose_name='接口请求类型'),
        ),
    ]

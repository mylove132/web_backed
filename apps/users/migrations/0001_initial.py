# Generated by Django 2.2.1 on 2019-05-27 12:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=20, unique=True, verbose_name='用户名')),
                ('email', models.EmailField(max_length=50, unique=True, verbose_name='邮箱')),
                ('password', models.CharField(max_length=100, verbose_name='用户密码')),
                ('user_type', models.IntegerField(choices=[(1, '普通用户'), (2, 'vip用户'), (3, '管理员用户')], default=1, verbose_name='用户类型')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
            options={
                'verbose_name': '用户',
                'db_table': 'entity_user',
            },
        ),
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=200, unique=True, verbose_name='token值')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='users.User')),
            ],
            options={
                'verbose_name': 'token值',
                'db_table': 'entity_token',
            },
        ),
    ]

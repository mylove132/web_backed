# Generated by Django 2.2.1 on 2019-05-29 18:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('md5', models.CharField(max_length=64, verbose_name='文件md5')),
                ('status', models.CharField(max_length=20, verbose_name='执行结果')),
                ('script', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Script')),
            ],
            options={
                'verbose_name': '历史记录',
                'db_table': 'entity_history',
            },
        ),
    ]

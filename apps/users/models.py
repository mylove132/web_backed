from django.db import models


class User(models.Model):
    USER_TYPE = (
        (1, '普通用户'),
        (2, 'vip用户'),
        (3, '管理员用户')
    )
    email = models.EmailField(max_length=50, verbose_name='邮箱', blank=False, unique=True)
    password = models.CharField(max_length=100, verbose_name='用户密码')
    user_type = models.IntegerField(choices=USER_TYPE, default=1, verbose_name='用户类型')
    create_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')

    class Meta:
        db_table = 'entity_user'
        verbose_name = '用户'


class Token(models.Model):
    token = models.CharField(max_length=200, verbose_name='token值', unique=True)
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'entity_token'
        verbose_name = 'token值'

from users.models import *


class Project(models.Model):
    ENV = (
        (1, 'dev'),
        (2, 'docker-dev'),
        (3, 'docker-hotfix'),
        (4, 'stress')
    )
    TYPE = (
        (1, '教师空间'),
        (2, '学生pad'),
        (3, '教师pad'),
        (4, '商城'),
        (5, 'OKAY+')
    )
    name = models.CharField(max_length=20, null=False, blank=True, verbose_name='项目名称')
    env = models.IntegerField(choices=ENV,default=1, verbose_name='项目环境')
    type = models.IntegerField(choices=TYPE,default=1, verbose_name='项目类型')
    desc = models.CharField(max_length=200, blank=True, verbose_name='项目描述')
    ctime = models.DateTimeField(auto_now_add=True, verbose_name='项目创建时间')
    update_time = models.DateTimeField(auto_now_add=True, verbose_name='项目更新时间')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'entity_project'


class Script(models.Model):
    REQUEST_TYPE = (
        (1, "GET"),
        (2, "POST"),
        (3, "DELETE")
    )
    PROCOTOL = (
        (1, "GET"),
        (2, "POST"),
        (3, "DELETE")
    )
    name = models.CharField(max_length=30, verbose_name='脚本名称')
    pre_number = models.IntegerField(verbose_name='并发数')
    pre_time = models.IntegerField(verbose_name='压测时长')
    url = models.CharField(max_length=200, verbose_name='压测url')
    time_out = models.IntegerField(default=5000, blank=True, verbose_name='超时时间')
    request_type = models.IntegerField(choices=REQUEST_TYPE,default=1, verbose_name='接口请求类型')
    protocol = models.IntegerField(choices=PROCOTOL,default=1, verbose_name='接口协议')
    ins = models.CharField(max_length=100, blank=True, verbose_name='dubbo接口名称')
    assert_text = models.CharField(max_length=50, blank=True, verbose_name='响应断言文本')
    method = models.CharField(max_length=30, blank=True, verbose_name='dubbo接口方法名')
    params = models.CharField(blank=True, max_length=200, verbose_name='压测接口参数值')
    param_type = models.CharField(blank=True, max_length=100, verbose_name='dubbo接口请求参数类型')
    cookie = models.CharField(max_length=300, blank=True, verbose_name='cookie')
    header = models.CharField(max_length=300, blank=True, verbose_name='header')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now_add=True, verbose_name='更新时间')
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'entity_script'
        verbose_name = '脚本'

# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import subprocess

from django.http import FileResponse, HttpResponse, StreamingHttpResponse
from rest_framework.views import APIView
from users.permissions import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from api.serializers import *
from api.util import http_jmx, constant, dubbo_jmx
import django_filters
from rest_framework import filters
import json
import requests
from django.utils.encoding import escape_uri_path
from kazoo.client import KazooClient
from urllib import parse


class CustomModelView(ModelViewSet):
    response = {}

    def update(self, request, *args, **kwargs):
        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            is_valid = serializer.is_valid(raise_exception=False)
            if not is_valid:
                return Response({'code': 3001, 'msg': '参数验证失败', 'data': serializer.errors})
            self.perform_update(serializer)

            if getattr(instance, '_prefetched_objects_cache', None):
                instance._prefetched_objects_cache = {}

            return Response({'code': 0, 'msg': 'OK', 'data': serializer.data})
        except Exception as e:
            self.response['code'] = -1
            self.response['msg'] = '未知异常'
            self.response['data'] = e
            return Response(self.response)

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(queryset, many=True)
            return Response({'code': 0, 'msg': 'OK', 'data': serializer.data})
        except Exception as e:
            self.response['code'] = -1
            self.response['msg'] = '未知异常'
            self.response['data'] = e
            return Response(self.response)

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)

            return Response({'code': 0, 'msg': 'OK', 'data': serializer.data})
        except Exception as e:
            self.response['code'] = -1
            self.response['msg'] = '未知异常'
            self.response['data'] = e
            return Response(self.response)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({'code': 0, 'msg': 'OK', 'data': '删除成功'})
        except Exception as e:
            self.response['code'] = -1
            self.response['msg'] = '未知异常'
            self.response['data'] = e
            return Response(self.response)

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            is_valid = serializer.is_valid(raise_exception=False)
            if not is_valid:
                return Response({'code': 3001, 'msg': '参数验证失败', 'data': serializer.errors})
            self.perform_create(serializer)
            return Response({'code': 0, 'msg': 'OK', 'data': {'id': serializer.data['id']}})
        except Exception as e:
            self.response['code'] = -1
            self.response['msg'] = '未知异常'
            self.response['data'] = e
            return Response(self.response)


class ProjectFilter(django_filters.FilterSet):
    class Meta:
        model = Project
        fields = ['env', 'type', 'user', ]


class ProjectModelViewSet(CustomModelView):
    authentication_classes = []
    permission_classes = []
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    filter_class = ProjectFilter
    search_fields = ('name',)
    queryset = Project.objects.order_by('-update_time')
    serializer_class = ProjectSerializer


class ScriptFilter(django_filters.FilterSet):
    class Meta:
        model = Script
        fields = ['project', 'user', 'protocol', ]


class ScriptModelViewSet(CustomModelView):
    permission_classes = [VipPermission, ]
    # authentication_classes = []
    queryset = Script.objects.order_by('-update_time')
    serializer_class = ScriptSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    filter_class = ScriptFilter
    search_fields = ('name',)


class HistoryFilter(django_filters.FilterSet):
    class Meta:
        model = History
        fields = ['user', 'script', ]


class HistoryModelViewSet(CustomModelView):
    permission_classes = []
    authentication_classes = []
    queryset = History.objects.order_by('-create_time')
    serializer_class = HistorySerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    filter_class = HistoryFilter
    search_fields = ('md5',)


class ReportView(APIView):
    response = {}
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        md5 = request._request.GET.get('md5')
        script_name = request._request.GET.get('script_name')
        history_id = request._request.GET.get('history_id')
        if not md5:
            self.response['code'] = 6001
            self.response['msg'] = '文件md5值不能为空'
            return Response(self.response)
        if not script_name:
            self.response['code'] = 6001
            self.response['msg'] = '脚本名称不能为空'
            return Response(self.response)
        if not history_id:
            self.response['code'] = 6001
            self.response['msg'] = 'history_id不能为空'
            return Response(self.response)

        history_obj = History.objects.filter(id=history_id, md5=md5).first()
        if not history_obj:
            self.response['code'] = 6002
            self.response['msg'] = 'history_id与md5不匹配'
            return Response(self.response)

        rtot_path = constant.REPORT_IMG_PATH + script_name + "_" + md5 + "_" + 'ResponseTimesOverTime.png'
        tps_path = constant.REPORT_IMG_PATH + script_name + "_" + md5 + "_" + 'TransactionsPerSecond.png'
        csv_path = constant.REPORT_CSV_PATH + script_name + "_" + md5 + '_AggregateReport.csv'
        if os.path.exists(tps_path) and os.path.exists(rtot_path) and os.path.exists(csv_path):
            file_content = ''
            with open(csv_path, 'r', encoding='utf-8') as file:
                file_content = file.readlines()
            self.response['code'] = 0
            self.response['msg'] = 'OK'
            self.response['data'] = {
                "history_id": history_obj.id,
                "urlList": {
                    "tps": "http://127.0.0.1:8086/" + script_name + "_" + md5 + "_" + 'TransactionsPerSecond.png',
                    "rtot": "http://127.0.0.1:8086/" + script_name + "_" + md5 + "_" + 'ResponseTimesOverTime.png',
                },
                "aggregate": file_content
            }
            return Response(self.response)
        else:
            s_path = constant.SHELL_PATH
            cmd = 'sh {} {}'.format(s_path, script_name + "_" + md5)
            with subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE) as p:
                while p.poll() is None:
                    out = p.stdout.readline()
                    out = str(out, encoding='utf-8')
                    print(out)
                    if os.path.exists(tps_path) and os.path.exists(rtot_path) and os.path.exists(csv_path):
                        file_content = ''
                        with open(csv_path, 'r', encoding='utf-8') as file:
                            file_content = file.readlines()
                        self.response['code'] = 0
                        self.response['msg'] = 'OK'
                        self.response['data'] = {
                            "history_id": history_obj.id,
                            "urlList": {
                                "tps": "http://127.0.0.1:8086/" + script_name + "_" + md5 + "_" + 'TransactionsPerSecond.png',
                                "rtot": "http://127.0.0.1:8086/" + script_name + "_" + md5 + "_" + 'ResponseTimesOverTime.png',
                            },
                            "aggregate": file_content
                        }
                        return Response(self.response)
            return Response({'code': -1, 'msg': '未知异常'})


class ReportLogView(APIView):
    response = {}
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        md5 = request._request.GET.get('md5')
        script_name = request._request.GET.get('script_name')
        history_id = request._request.GET.get('history_id')
        if not md5:
            self.response['code'] = 6001
            self.response['msg'] = '文件md5值不能为空'
            return Response(self.response)
        if not script_name:
            self.response['code'] = 6001
            self.response['msg'] = '脚本名称不能为空'
            return Response(self.response)
        if not history_id:
            self.response['code'] = 6001
            self.response['msg'] = 'history_id不能为空'
            return Response(self.response)

        history_obj = History.objects.filter(id=history_id, md5=md5).first()
        if not history_obj:
            self.response['code'] = 6002
            self.response['msg'] = 'history_id与md5不匹配'
            return Response(self.response)

        if os.path.exists(
                constant.JMETER_LOG + script_name + "_" + md5 + '.log'):
            with open(constant.JMETER_LOG + script_name + "_" + md5 + '.log', 'r', encoding='utf-8') as logfile:
                logs = logfile.read()
            self.response['code'] = 0
            self.response['msg'] = 'OK'
            self.response['data'] = {
                "log": logs
            }
            return Response(self.response)
        else:
            self.response['code'] = 6003
            self.response['msg'] = '查询的报告日志不存在'
            return Response(self.response)


class RunScript(APIView):
    response = {}
    permission_classes = [VipPermission, ]

    def post(self, request):
        user = request.data.get('user')
        pk = request.data.get('id')
        data = Script.objects.filter(pk=pk).first()
        from api.util.redis_cli import exec_file_redis
        if exec_file_redis.exists('exec_jmx_index'):
            if int(exec_file_redis.get('exec_jmx_index')) >= 2:
                self.response['code'] = 5001
                self.response['msg'] = '目前执行数已达最多，请稍后再试'
                self.response['data'] = ''
                return Response(self.response)
            else:
                exec_file_redis.set('exec_jmx_index', str(int(exec_file_redis.get('exec_jmx_index')) + 1))
        else:
            exec_file_redis.set('exec_jmx_index', '1')

        if exec_file_redis.exists('exec_jmx_script_id_' + str(pk)):
            self.response['code'] = 5002
            self.response['msg'] = '执行的脚本已存在'
            self.response['data'] = ''
            return Response(self.response)

        else:
            exec_file_redis.set('exec_jmx_script_id_' + str(pk), pk)
        import datetime
        import time
        import hashlib
        time_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        st = time.strptime(time_now, '%Y-%m-%d %H:%M:%S')
        time_tramp = time.mktime(st)

        def md5(name, salt=str(time_tramp)):
            md5 = hashlib.md5(bytes(name, encoding='utf-8'))
            md5.update(bytes(salt, encoding='utf-8'))
            return md5.hexdigest()

        pre_time = data.pre_time
        pre_number = data.pre_number
        # 请求的接口名称
        name = data.name
        type_dict = {1: "GET", 2: "POST", 3: "DELETE"}
        # 获取请求方式
        request_type = type_dict[data.request_type]
        # 获取请求的url
        url = data.url
        # 获取请求的超时时间
        time_out = data.time_out
        # 获取请求的参数
        param = data.params
        # 获取请求的断言结果
        assert_text = data.assert_text
        # 获取请求的cookie信息
        cookie = data.cookie
        # 获取请求的header信息
        header = data.header
        # 获取请求的监控ip地址
        ip = data.ip
        # 获取请求的监控端口
        port = data.port
        # 获取dubbo接口
        ins = data.ins
        # 获取dubbo方法
        method = data.method
        # 获取version
        version = data.version
        # 获取dubbo方法
        param_type = data.param_type
        # 获取接口的环境
        env = data.project.env
        if env == 1:
            zkAddress = '10.10.6.3:2181'
        elif env == 2:
            zkAddress = '172.18.4.48:2181'
        elif env == 3:
            zkAddress = '10.10.1.7:2181'
        if cookie:
            cookie = json.loads(cookie)
        else:
            cookie = {}
        if header:
            header = json.loads(header)
        else:
            header = {}
        filename = md5(name)
        isIp = False
        # 是否监控服务器
        if ip != 'localhost' and ip != None and ip != '':
            isIp = True
        dubbo_f_path = constant.JMX_PATH + name + '_' + filename + ".jmx";
        if data.protocol == 1:
            # 创建http协议的jmx文件
            create_http_jmx_file(dubbo_f_path, url, pre_time=pre_time,
                                 pre_num=pre_number,
                                 interface_name=name, request_type=request_type, time_out=time_out, param=param,
                                 cookie=cookie,
                                 header=header, assert_text=assert_text, isIp=isIp, ip=ip, port=port)

        elif data.protocol == 2:
            create_dubbo_jmx_file(dubbo_f_path, ins=ins, method=method,
                                  param_type=param_type, pre_time=pre_time, pre_num=pre_number, zkAddress=zkAddress,
                                  version=version, interface_name=name, time_out=time_out, assert_text=assert_text,
                                  ip=ip, port=port, isIp=isIp, param=param)

        if os.path.exists(dubbo_f_path):
            cmd = '{} -n -t {} -l {} -j {}'.format(constant.JMETER_PATH,
                                                   dubbo_f_path,
                                                   constant.JTL_PATH + name + '_' + filename + ".jtl",
                                                   constant.JMETER_LOG + name + '_' + filename + ".log")
            with subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE) as p:
                while p.poll() is None:
                    out = p.stdout.readline()
                    out = str(out, encoding='utf-8')
                    if out != "":
                        from asgiref.sync import async_to_sync
                        from channels.layers import get_channel_layer
                        channel_layer = get_channel_layer()
                        async_to_sync(channel_layer.group_send)("chat_2202", {
                            "type": "chat.message",
                            "code": 0,
                            "message": out,
                        })
                        if out.find('end of run') != -1:
                            async_to_sync(channel_layer.group_send)("chat_2202", {
                                "type": "chat.message",
                                "code": 2,
                                "message": 'finish',
                            })

        exec_file_redis.delete('exec_jmx_script_id_' + str(pk))
        exec_file_redis.set('exec_jmx_index', str(int(exec_file_redis.get('exec_jmx_index')) - 1))

        history = History(md5=filename, status='success', script_id=pk, user_id=user)
        history.save()
        return Response({"code": 0, "msg": 'OK'})


class TestRequestApiView(APIView):
    response = {}
    authentication_classes = []

    def get(self, request):
        url = request._request.GET.get('url')
        protocol = request._request.GET.get('protocol')
        cookie = request._request.GET.get('cookie')
        header = request._request.GET.get('header')
        request_type = request._request.GET.get('request_type')
        params = request._request.GET.get('params')
        type_dict = {1: "GET", 2: "POST", 3: "DELETE"}

        ins = request._request.GET.get('ins')
        method = request._request.GET.get('method')
        param_type = request._request.GET.get('param_type')
        version = request._request.GET.get('version')
        time_out = request._request.GET.get('time_out')
        env = request._request.GET.get('env')

        if not time_out:
            time_out = 5000

        headers = {}
        cookies = {}
        param = {}
        if not header:
            header = headers
        else:
            header_dict = json.loads(header)
            for h in header_dict:
                k = h['headerKey']
                v = h['headerValue']
                headers[k] = v
        if not cookie:
            cookie = cookies
        else:
            cookie_dict = json.loads(cookie)
            for c in cookie_dict:
                k = c['cookieKey']
                v = c['cookieValue']
                cookies[k] = v

        if not params:
            params = param
        elif params.find('paramskey') != -1:
            params_dict = json.loads(params)
            for c in params_dict:
                k = c['paramskey'].replace(' ', '')
                v = c['paramsvalue'].replace(' ', '')
                param[k] = v
        else:
            param = params.replace(' ', '')

        if not protocol:
            protocol = 1

        if not request_type:
            request_type = 1

        if 'Content-Type' in param:
            if param['Content-Type'] == 'application/json':
                param = json.loads(param)

        if int(protocol) == 1:
            if not url:
                self.response['code'] = 7001
                self.response['msg'] = '测试url不能为空'
                self.response['data'] = ''
                return Response(self.response)
            print(type_dict[int(request_type)])
            print(param)
            print(url)
            print(headers)
            print(cookies)
            response = requests.request(type_dict[int(request_type)], data=param, url=url, headers=headers,
                                        cookies=cookies)
            self.response['code'] = 0
            self.response['msg'] = 'OK'
            self.response['data'] = response.text
            return Response(self.response)


class DubboRequestApiView(APIView):
    response = {}
    services = []
    authentication_classes = []

    def get(self, request):
        protocol = request._request.GET.get('protocol')
        env = request._request.GET.get('env')
        if protocol and env:
            if not self.services:
                self.services = []
            if int(protocol) == 2 and int(env) == 1:
                try:
                    zk = KazooClient(hosts='10.10.6.3:2181')
                    zk.start()
                except Exception as e:
                    self.response['code'] = -1
                    self.response['msg'] = 'zk连接异常'
                    self.response['data'] = ''
                    return Response(self.response)

                @zk.ChildrenWatch("/dubbo")
                def watch_children(children):
                    self.services.append(children)

                self.response['code'] = 0
                self.response['msg'] = 'OK'
                self.response['data'] = self.services
                return Response(self.response)
            elif int(protocol) == 2 and int(env) == 2:
                try:
                    zk = KazooClient(hosts='172.18.4.48:2181')
                    zk.start()
                except Exception as e:
                    self.response['code'] = -1
                    self.response['msg'] = 'zk连接异常'
                    self.response['data'] = ''
                    return Response(self.response)

                @zk.ChildrenWatch("/dubbo")
                def watch_children(children):
                    self.services.append(children)

                self.response['code'] = 0
                self.response['msg'] = 'OK'
                self.response['data'] = self.services
                return Response(self.response)
            elif int(protocol) == 2 and int(env) == 3:
                try:
                    zk = KazooClient(hosts='10.10.1.7:2181')
                    zk.start()
                except Exception as e:
                    self.response['code'] = -1
                    self.response['msg'] = 'zk连接异常'
                    self.response['data'] = ''
                    return Response(self.response)

                @zk.ChildrenWatch("/dubbo")
                def watch_children(children):
                    self.services.append(children)

                self.response['code'] = 0
                self.response['msg'] = 'OK'
                self.response['data'] = self.services
                return Response(self.response)
            else:
                self.response['code'] = 8001
                self.response['msg'] = '暂时不接受别的环境'
                self.response['data'] = ''
                return Response(self.response)


class DownloadReportView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        response = {}
        md5 = request._request.GET.get('md5')
        script_name = request._request.GET.get('script_name')
        history_id = request._request.GET.get('history_id')
        print(md5)
        print(script_name)
        if not md5:
            response['code'] = 6001
            response['msg'] = '文件md5值不能为空'
            return Response(response)
        if not script_name:
            response['code'] = 6001
            response['msg'] = '脚本名称不能为空'
            return Response(response)
        if not history_id:
            response['code'] = 6001
            response['msg'] = 'history_id不能为空'
            return Response(response)

        history_obj = History.objects.filter(id=history_id, md5=md5).first()
        if not history_obj:
            response['code'] = 6002
            response['msg'] = 'history_id与md5不匹配'
            return Response(response)
        file_path = constant.REPORT_CSV_PATH + script_name + "_" + md5 + '_AggregateReport.csv'
        if os.path.exists(file_path):
            download_name = file_path
            the_file_name = str(download_name).split("/")[-1]  # 显示在弹出对话框中的默认的下载文件名
            responseContent = StreamingHttpResponse(readFile(file_path))
            responseContent['Content-Type'] = 'application/octet-stream'
            responseContent['Content-Disposition'] = 'attachment;filename={}'.format(escape_uri_path(the_file_name))
            return responseContent
        else:
            response['code'] = 6003
            response['msg'] = '尚未生成报告，请先生成报告'
            return Response(response)


def readFile(filename, chunk_size=512):
    """
    缓冲流下载文件方法
    :param filename:
    :param chunk_size:
    :return:
    """
    with open(filename, 'rb') as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break


class DubboMethodApiView(APIView):
    response = {}
    methods = []

    def get(self, request):
        protocol = request._request.GET.get('protocol')
        env = request._request.GET.get('env')
        ins = request._request.GET.get('ins')
        if protocol and env:
            if int(protocol) == 2 and int(env) == 1:

                zk = KazooClient(hosts='10.10.6.3:2181')
                zk.start()

                @zk.ChildrenWatch("/dubbo/" + ins + "/providers")
                def watch_children(children):
                    urldata = parse.unquote(str(children))
                    result = parse.urlparse(urldata)
                    query_dict = parse.parse_qs(result.query)
                    methods = query_dict.get('methods', [])
                    for method in methods:
                        method = method.replace('\'', '')
                        self.methods.append(method.split(','))

                self.response['code'] = 0
                self.response['msg'] = 'OK'
                self.response['data'] = {"methods": self.methods}
                return Response(self.response)
            elif int(protocol) == 2 and int(env) == 2:
                zk = KazooClient(hosts='172.18.4.48:2181')
                zk.start()

                @zk.ChildrenWatch("/dubbo/" + ins + "/providers")
                def watch_children(children):
                    urldata = parse.unquote(str(children))
                    result = parse.urlparse(urldata)
                    query_dict = parse.parse_qs(result.query)
                    methods = query_dict.get('methods', [])
                    for method in methods:
                        method = method.replace('\'', '')
                        self.methods.append(method.split(','))

                self.response['code'] = 0
                self.response['msg'] = 'OK'
                self.response['data'] = {"methods": self.methods}
                return Response(self.response)
            elif int(protocol) == 2 and int(env) == 3:
                zk = KazooClient(hosts='10.10.1.7:2181')
                zk.start()

                @zk.ChildrenWatch("/dubbo/" + ins + "/providers")
                def watch_children(children):
                    urldata = parse.unquote(str(children))
                    result = parse.urlparse(urldata)
                    query_dict = parse.parse_qs(result.query)
                    methods = query_dict.get('methods', [])
                    for method in methods:
                        method = method.replace('\'', '')
                        self.methods.append(method.split(','))

                self.response['code'] = 0
                self.response['msg'] = 'OK'
                self.response['data'] = {"methods": self.methods}
                return Response(self.response)
            else:
                self.response['code'] = 8001
                self.response['msg'] = '暂时不接受别的环境'
                self.response['data'] = ''
                return Response(self.response)


def create_http_jmx_file(filepath, url, pre_time=200, pre_num=200, interface_name='http请求', request_type='GET',
                         time_out=5000, param='', assert_text='', cookie={}, header={}, isIp=False, ip='localhost',
                         port=4444):
    jmx_file_content = http_jmx.jmx_header_setting() + http_jmx.jmx_control_seeting(pre_num,
                                                                                    pre_time) + http_jmx.jmx_http_setting(
        url, interface_name=interface_name, request_type=request_type, timeOut=time_out,
        params=param) + http_jmx.jmx_response_assert(
        assert_text=assert_text) + http_jmx.jmx_see_result_control() + http_jmx.result_polymerization_control() + \
                       http_jmx.requestid_bean_shell_control() + http_jmx.cookie_control(
        cookies=cookie, url=url) + http_jmx.header_control(header=header) + http_jmx.response_time_over_time() + \
                       http_jmx.transactions_per_second(True) + http_jmx.perfmon_metrics_collertor(ip=ip, port=port,
                                                                                                   enable=isIp) + http_jmx.jmx_end()
    with open(filepath, 'w', encoding='utf-8') as jmx_file:
        jmx_file.write(jmx_file_content)


def create_dubbo_jmx_file(filepath, ins, method, param_type, pre_time=200, pre_num=200, zkAddress='10.10.6.3:2181',
                          version='3.0.0', interface_name='dubbo请求',
                          time_out=5000, param='', assert_text='', isIp=False, ip='localhost',
                          port=4444):
    jmx_file_content = dubbo_jmx.head_setting() + dubbo_jmx.run_crontrol_setting(pre_number=pre_num,
                                                                                 pre_time=pre_time) + dubbo_jmx.dubbo_Sample_Gui_setting(
        ins_name=interface_name,
        zkAddress=zkAddress, time_out=time_out, version=version, interface=ins, method=method, paramType=param_type,
        paramValue=param) + dubbo_jmx.watch_result_tree_setting() + dubbo_jmx.result_collector_setting() + dubbo_jmx.response_assertion_setting(
        assert_text=assert_text) + dubbo_jmx.response_TimesOver_TimeGui_setting() + dubbo_jmx.transactions_PerSecond_Gui_setting() + http_jmx.perfmon_metrics_collertor \
                           (ip=ip, port=port, enable=isIp) + dubbo_jmx.end_setting()
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(str(jmx_file_content))

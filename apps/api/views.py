# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework.views import APIView
from users.permissions import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from api.serializers import *
import django_filters
from rest_framework import filters


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
    # permission_classes = [VipPermission,]
    permission_classes = [VipPermission, ]
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
    queryset = Script.objects.order_by('-update_time')
    serializer_class = ScriptSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    filter_class = ScriptFilter
    search_fields = ('name',)


class RunScript(APIView):
    # permission_classes = [VipPermission, ]
    response = {}

    def post(self, request):
        file_path = 'E:\\workspace\\jmeter\\jmx\\jie.jmx'
        jmeter_path = 'E:\\jemter\\apache-jmeter-3.3\\bin\\jmeter.bat'
        jtl_path = 'E:\\workspace\\jmeter\\jtl\\test01.jtl'
        log_path = 'E:\\workspace\\jmeter\\log\\test01.log'
        from api.redis_cli import exec_file_redis
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
        import os
        cmd = '{} -n -t {} -l {} -j {}'.format(jmeter_path, file_path, jtl_path, log_path)
        with os.popen(cmd,'r') as p:
            res = p.read()
            for line in res.splitlines():
                print(line)

        return Response()

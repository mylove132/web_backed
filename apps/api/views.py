# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from api.serializers import *
from users.permissions import *


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


class ProjectModelViewSet(CustomModelView):
    permission_classes = [VipPermission,]
    queryset = Project.objects.order_by('-ctime')
    serializer_class = ProjectSerializer


class ScriptModelViewSet(CustomModelView):
    queryset = Script.objects.order_by('-create_time')
    serializer_class = ScriptSerializer


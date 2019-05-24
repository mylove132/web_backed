# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import JsonResponse
from rest_framework.views import APIView
from api.serializers import *


class ProjectAPIView(APIView):
    authentication_classes = []

    def get(self, request):
        response = {}
        if request._request.GET.get('id'):
            try:
                project = Project.objects.get(pk=request._request.GET.get('id'))
            except Exception as e:
                response['code'] = 2005
                response['msg'] = '查询项目不存在'
                response['data'] = ''
                return JsonResponse(response)
            proserializer = ProjectSerializer(project)
            response['code'] = 0
            response['msg'] = 'OK'
            response['data'] = proserializer.data
            return JsonResponse(response)
        else:
            project = Project.objects.all()
            proserializer = ProjectSerializer(project, many=True)
            response['code'] = 0
            response['data'] = 'OK'
            response['data'] = proserializer.data
            return JsonResponse(response)

    def post(self, request):
        response = {}
        data = request.data
        projectserializer = ProjectSerializer(data=data)
        if projectserializer.is_valid():
            projectserializer.save()
            response['code'] = 0
            response['data'] = 'OK'
            response['data'] = projectserializer.data
            return JsonResponse(response)

    def delete(self, request):
        response = {}
        project_id = request._request.GET.get('id')
        if not project_id:
            response['code'] = 1008
            response['msg'] = '请传入项目id'
            response['data'] = ''
            return JsonResponse(response)
        try:
            pro_obj = Project.objects.get(id=request._request.GET.get('id'))
        except Exception as e:
            response['code'] = 2007
            response['msg'] = '删除项目不存在'
            response['data'] = ''
            return JsonResponse(response)

        print(pro_obj)
        if pro_obj:
            (deleted, result) = pro_obj.delete()
            if deleted:
                response['code'] = 0
                response['msg'] = 'OK'
                response['data'] = None
                return JsonResponse(response)
            else:
                response['code'] = 2006
                response['msg'] = '删除项目失败'
                response['data'] = result
                return JsonResponse(response)

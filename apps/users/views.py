# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import JsonResponse
from rest_framework.views import APIView
import hashlib
from users.serializers import *
from api.views import CustomModelView


def md5(name, salt='okay'):
    md5 = hashlib.md5(bytes(name, encoding='utf-8'))
    md5.update(bytes(salt, encoding='utf-8'))
    return md5.hexdigest()


# 用于登录
class UserLoginApiView(APIView):
    authentication_classes = []

    def post(self, request, format=None):
        response = {}
        data = request.data
        email = data.get('email')
        password = data.get('password')
        print(request.data)
        if email:
            user = User.objects.filter(email=email).first()
            if not user:
                response['code'] = 1004
                response['msg'] = '用户名错误'
                response['data'] = ''
                return JsonResponse(response)
            if user.password == password:
                token = md5(user.email, salt=timezone.now().strftime('%Y-%m-%d %H:%M:%S'))
                Token.objects.update_or_create(user=user,
                                               defaults={'token': token, 'update_time': timezone.now})
                response['code'] = 0
                response['msg'] = 'OK'
                response['data'] = {
                    "token": token,
                    'email': user.email
                }

                return JsonResponse(response)
            else:
                response['code'] = 1001
                response['msg'] = '密码错误'
                response['data'] = ''
                return JsonResponse(response)

        response['code'] = 1005
        response['msg'] = '用户邮箱不能为空'
        return JsonResponse(response)


class UserModelViewSet(CustomModelView):
    queryset = User.objects.order_by('-create_time')
    serializer_class = UserSerializer

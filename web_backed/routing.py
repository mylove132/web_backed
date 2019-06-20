#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author:wd

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import business.routing

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            business.routing.websocket_urlpatterns# 指明路由文件是devops/routing.py
        )
    ),
})
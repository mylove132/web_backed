#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author:wd
from django.conf.urls import url

from business import consumer

websocket_urlpatterns = [
    url(r'^ws/deploy/(?P<script_id>[^/]+)/$', consumer.DeployResult)
]
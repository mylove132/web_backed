#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author:wd

from channels.generic.websocket import AsyncWebsocketConsumer
import json

class DeployResult(AsyncWebsocketConsumer):
    async def connect(self):
        # ["kwargs"]
        self.service_uid = self.scope["url_route"]
        self.chat_group_name = 'chat_%s' % '2202'
        # 收到连接时候处理，
        await self.channel_layer.group_add(
            self.chat_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # 关闭channel时候处理
        await self.channel_layer.group_discard(
            self.chat_group_name,
            self.channel_name
        )

    # 收到消息
    async def receive(self, text_data):
        print(text_data)
        text_data_json = json.loads(text_data)
        message = text_data_json['test']
        print("收到消息--》",message)
        # # 发送消息到组
        # await self.channel_layer.group_send(
        #     self.chat_group_name,
        #     {
        #         'type': 'chat.message',
        #         'message': message
        #     }
        # )

    # 处理客户端发来的消息
    async def chat_message(self, event):
        message = event['message']
        code = event['code']
        # 发送消息到 WebSocket
        await self.send(text_data=json.dumps({
            "code":code,
            'message': message
        }))

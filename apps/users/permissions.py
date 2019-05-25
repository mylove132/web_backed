# coding=utf-8
from rest_framework import permissions


class CommonPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.user_type != 1:
            return False
        return True


class VipPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.user_type != 2:
            return False
        return True


class AdminPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.user_type != 3:
            return False
        return True
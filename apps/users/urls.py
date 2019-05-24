from django.conf.urls import url, include
# 定义路由
from rest_framework.routers import DefaultRouter

from users import views

router = DefaultRouter()

router.register(r'user', views.UserModelViewSet, base_name='user')

urlpatterns = [
    url('^login/$',views.UserLoginApiView.as_view()),
    url('^', include(router.urls)),
    # url('^', view=views.UserModelViewSet.as_view({'post':'create',})),
]
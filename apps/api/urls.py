from django.conf.urls import url, include
# 定义路由
from rest_framework.routers import DefaultRouter

from api import views

router = DefaultRouter()

router.register(r'project', views.ProjectModelViewSet, base_name='project')
router.register(r'script', views.ScriptModelViewSet, base_name='script')

urlpatterns = [
    url(r'^project/$',views.ProjectModelViewSet.as_view({'get':'list','post':'create'})),
    url('^', include(router.urls)),
]
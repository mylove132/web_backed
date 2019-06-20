from django.conf.urls import url, include
# 定义路由
from rest_framework.routers import DefaultRouter

from api import views

router = DefaultRouter()

router.register(r'project', views.ProjectModelViewSet, base_name='project')
router.register(r'script', views.ScriptModelViewSet, base_name='script')
router.register(r'history', views.HistoryModelViewSet, base_name='history')
urlpatterns = [
    url(r'^project/$',views.ProjectModelViewSet.as_view({'get':'list','post':'create'})),
    url(r'^script/$',views.ScriptModelViewSet.as_view({'get':'list','post':'create'})),
    url(r'^history/$',views.HistoryModelViewSet.as_view({'get':'list','post':'create'})),
    url('^', include(router.urls)),
    url('^exec/script',views.RunScript.as_view()),
    url('^report',views.ReportView.as_view()),
    url('^logreport',views.ReportLogView.as_view()),
    url('^testRequest',views.TestRequestApiView.as_view()),
    url('^dubbo/service',views.DubboRequestApiView.as_view()),
    url('^dubbo/method', views.DubboMethodApiView.as_view()),
    url('^download', views.DownloadReportView.as_view()),
]
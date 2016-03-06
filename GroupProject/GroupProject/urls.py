from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from webinterface import views
from rest_framework import routers
from webinterface.api import *
from . import settings

router = routers.SimpleRouter()
router.register(r'^projects', ProjectList, base_name='project-list')
router.register(r'^analyses', AnalysisList, base_name='analysis-list')
router.register(r'^turbines', TurbineList, base_name='turbine-list')
router.register(r'^project-analyses', ProjectAnalysisList)


urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^$', views.main),

    url(r'^project/(?P<title>[A-Z-a-z-0-9]+)/$', views.project_view, name='project_view'),

    url(r'^upload-site-calibration', views.test_upload, name='test_upload'),

    url(r'^api/v1/', include(router.urls)),


    url(r'^test$', views.test, name='test'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
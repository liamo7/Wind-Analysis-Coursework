"""GroupProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from webinterface.views import *
from rest_framework_nested import routers
from GroupProject import settings

router = routers.SimpleRouter()
router.register(r'projects', ProjectViewSet)
router.register(r'turbines', TurbineViewSet)
router.register(r'analyses', AnalysisViewSet)

urlpatterns = [

    url(r'^api/v1/', include(router.urls)),
    url(r'^api/v1/columntypes', ColumnTypeViewSet.as_view()),
    url(r'^api/v1/valuetypes', ValueTypeViewSet.as_view()),

    url(r'^admin/', admin.site.urls),
    url(r'^.*$', index, name='index'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

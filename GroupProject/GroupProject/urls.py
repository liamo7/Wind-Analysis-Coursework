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
from django.contrib import admin
from webinterface import views
from webinterface.api import ProjectList, ProjectDetail, AnalysisList, AnalysisDetail, ProjectAnalysisList

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^$', views.main),

    url(r'^project/(?P<title>[A-Z-a-z-0-9]+)/$', views.project_view, name='project_view'),
    url(r'^project/create', views.create_project, name='create_project'),


    url(r'^test/$', views.testmain),

    url(r'^test/project/$', ProjectList.as_view(), name='project-list'),
    url(r'^test/project/(?P<title>.+)/$', ProjectDetail.as_view(), name='project-detail'),

    url(r'^test/project-analysis/(?P<title>.+)/$', ProjectAnalysisList.as_view(), name='project-analysis-list'),
    url(r'^test/analysis/$', AnalysisList.as_view(), name='analysis-list'),
    url(r'^test/analysis/(?P<title>.+)/$', AnalysisDetail.as_view(), name='analysis-detail')

]

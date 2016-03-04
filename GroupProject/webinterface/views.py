from django.shortcuts import render, redirect
from .projects import *
from .analyses import getAnalysisFromProject
from .forms import ProjectForm, UploadFileForm
from .utils import readFromCsv
from django.http import HttpResponse


def main(request):

    context = {
        'page': 'home'
    }

    return render(request, 'webinterface/base.html', context)


def project_view(request, title):

    project = getProjectByTitle(title)
    analyses = getAnalysisFromProject(project)

    context = {
        'page': 'project-view',
        'sidebar_title': project.title,
        'sidebar_object': 'project-obj',
        'sidebar_data': analyses
    }

    return render(request, 'webinterface/base.html', context)


def test_upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handleFileUpload(request.FILES['file'])
            return redirect('project_view', title='Project1')
    else:
        form = UploadFileForm()

    context = {
        'page': 'upload',
        'sidebar_title': 'Project List',
        'sidebar_object': 'project-list',
        'sidebar_data': getAllProjects(),
        'form': form
    }

    return render(request, 'webinterface/base.html', context)


def handleFileUpload(file):
    project = getProjectByTitle('Project1')
    project.site_calibration_file = file
    project.save()


"""
    Returns for sidebar from render

    sidebar-title - sidebar title
    sidebar-files - list of dirs and files to display in sidebar

    toolbar-options - lists of buttons to show on toolbar

    page - the page that should be displayed

    projects - list of created projects in db
    project - current project instance, use dot notation on it

"""


from .models import Turbine
def test(request):

    turbine = Turbine.objects.get_or_create(name='Nordex', manufacturer='Davis', model='N-90', diameter=20.5, hub_height=15.2)
    turbine[0].setBins([0,0.5,1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6,6.5,7,7.5,8,8.5,9,9.5,10,10.5,11,11.5,12,12.5,13,13.5,14,14.5,15,15.5,16,16.5,17,17.5,18,18.5,19,19.5,20,20.5,21,21.5,22,22.5,23,23.5,24,24.5,25,25.5])
    turbine[0].setPowerInKillowats([0,0,0,0,0,0,0,29,76,136,207,292,390,504,635,787,958,1147,1352,1570,1799,2036,2231,2368,2454,2496,2500,2500,2500,2500,2500,2500,2500,2500,2500,2500,2500,2500,2500,2500,2500,2500,2500,2500,2500,2500,2500,2500,2500,2500,2500,0])

    dict = turbine[0].createPowerCurveDict()

    print(dict['bin'])
    print(dict['powerInKilowatts'])

    return HttpResponse("Test")
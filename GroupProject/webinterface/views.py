from django.shortcuts import render, redirect
from .projects import *
from .analyses import getAnalysisFromProject
from .forms import ProjectForm, UploadFileForm
from .utils import readFromCsv


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
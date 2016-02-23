from django.shortcuts import render, redirect
from .projects import *
from .analyses import getAnalysisFromProject
from .forms import ProjectForm


def main(request):

    context = {
        'page': 'home',
        'sidebar_title': 'Project List',
        'sidebar_object': 'project-list',
        'sidebar_data': getAllProjects()
    }

    return render(request, 'webinterface/base.html', context)


def testmain(request):
    return render(request, 'webinterface/testbase.html')


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


def create_project(request):

    if request.method == 'POST':
        form = ProjectForm(request.POST)

        if form.is_valid():
            title = createProjectItem(form.cleaned_data['title'])
            return redirect('project_view', title=title)
    else:
        form = ProjectForm()

    context = {
        'page': 'create-project',
        'sidebar_title': 'Project List',
        'sidebar_object': 'project-list',
        'sidebar_data': getAllProjects(),
        'form': form
    }

    return render(request, 'webinterface/base.html', context)


"""
    Returns for sidebar from render

    sidebar-title - sidebar title
    sidebar-files - list of dirs and files to display in sidebar

    toolbar-options - lists of buttons to show on toolbar

    page - the page that should be displayed

    projects - list of created projects in db
    project - current project instance, use dot notation on it

"""
from django.shortcuts import render, redirect
from .models import Project, Analysis
from .projects import get_projects, get_project_by_title, create_project_item
from .analyses import get_analyses_from_project
from GroupProject import settings
from .forms import ProjectForm


def main(request):

    context = {
        'page': 'home',
        'sidebar_title': 'Project List',
        'sidebar_object': 'project-list',
        'sidebar_data': get_projects()
    }

    return render(request, 'webinterface/base.html', context)


def print_all_files_in_dir():
    import os
    for r, d, f in os.walk(settings.BASE_DIR):
        for file in f:
            print(os.path.join(settings.BASE_DIR, file))


def project_view(request, title):

    project = get_project_by_title(title)
    analyses = get_analyses_from_project(project)

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
            title = create_project_item(form.cleaned_data['title'])
            return redirect('project_view', title=title)
    else:
        form = ProjectForm()

    context = {
        'page': 'create-project',
        'sidebar_title': 'Project List',
        'sidebar_object': 'project-list',
        'sidebar_data': get_projects(),
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
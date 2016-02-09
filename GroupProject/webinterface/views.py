from django.shortcuts import render
from django.http import HttpResponse
import sys, os
from .models import Project, Analysis
from GroupProject import settings


def main(request):

    projects = getProjects()

    project1 = projects[0]
    analyses = Analysis.objects.filter(project=project1).all()

    return render(request, 'webinterface/base.html', {'projects': projects, 'proj': project1, 'analysis': analyses})


def printAllFilesWithinBaseDir():
    for r, d, f in os.walk(settings.BASE_DIR):
        for file in f:
            print(os.path.join(settings.BASE_DIR, file))


def projectView(request, title):

    print(title)

    project = Project.objects.get(title=title)
    print(project.title)
    analyses = Analysis.objects.filter(project=project).all()

    return render(request, 'webinterface/base.html', {'project': project, 'analyses': analyses, 'projects': getProjects()})


def getProjects():
    return Project.objects.all()

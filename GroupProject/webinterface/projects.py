from .models import Project
import os
from GroupProject import settings


def getAllProjects():
    return Project.objects.all()


def getProjectByTitle(title):
    return Project.objects.get(title=title)


def createProjectItem(title):
    project = Project.objects.create(title=title)
    project.save()

    directory = settings.MEDIA_ROOT + '/' + project.title

    if not os.path.exists(directory):
        os.makedirs(directory)

    return project.title

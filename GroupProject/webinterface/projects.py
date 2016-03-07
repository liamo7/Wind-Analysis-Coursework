from .models import Project
import os
from GroupProject import settings


def getAllProjects():
    return Project.objects.all()


def getProjectByTitle(title):
    return Project.objects.get(title=title)


def createProjectItem(project):

    directory = settings.MEDIA_ROOT + '/' + project.title

    if project.site_calibration_allowed:
        os.makedirs(directory + '/site_calibration')
    elif not os.path.exists(directory):
        os.makedirs(directory)


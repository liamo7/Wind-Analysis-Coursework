from .models import Project


def get_projects():
    return Project.objects.all()


def get_project_by_title(title):
    return Project.objects.get(title=title)


def create_project_item(title):
    project = Project.objects.create(title=title)
    project.save()
    return project.title

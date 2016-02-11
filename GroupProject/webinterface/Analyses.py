from .models import Analysis


def get_all_analyses():
    return Analysis.objects.all()


def get_analysis_from_title(title):
    return Analysis.objects.get(title=title)


def get_analyses_from_project(project):
    return Analysis.objects.filter(project=project)


def create_analysis(title):
    analysis = Analysis.objects.create(title=title).save()
    return analysis.title
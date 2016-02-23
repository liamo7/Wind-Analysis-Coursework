from .models import Analysis


def getAllAnalyses():
    return Analysis.objects.all()


def getAnalysisFromTitle(title):
    return Analysis.objects.get(title=title)


def getAnalysisFromProject(project):
    return Analysis.objects.filter(project=project)


def createAnalysis(title):
    analysis = Analysis.objects.create(title=title).save()
    return analysis.title

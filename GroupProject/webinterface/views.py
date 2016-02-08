from django.shortcuts import render
from django.http import HttpResponse


def main(request):
    return render(request, 'webinterface/base.html')

def index(request):
    return HttpResponse("Index")

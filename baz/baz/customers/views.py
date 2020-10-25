from django.shortcuts import render
from django.http import HttpResponse
import json


# Create your views here.
def sendmail(request):
    signature = request.POST.get("param", "")

    return HttpResponse("hi")

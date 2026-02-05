from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.conf import settings
from django.http import HttpResponse,FileResponse
import os



def app_docs(request):
    return render(request, 'document/index.html',{'project_version':settings.PROJECT_VERSION, 'project_name':settings.PROJECT_NAME})

def user_guide(request):
    return render(request, 'document/user_guide.html')


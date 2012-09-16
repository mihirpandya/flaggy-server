import os
from jinja2 import Environment, ChoiceLoader, FileSystemLoader
from doppio.models import User
from json import dumps
from datetime import datetime
from django.http import HttpResponse
from doppio import jinja2python
from jinja2python import render_to_response, render_to_string
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

def home_page(request):
    """ Simple Hello World View """
    print """Hello"""
    return render_to_response("index.html", context={"title":"First Render"})

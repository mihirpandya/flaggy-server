import os
from jinja2 import Environment, ChoiceLoader, FileSystemLoader
from doppio.models import User
from json import dumps
from datetime import datetime
from django.http import HttpResponse
from django.template import loader, Context
from . import jinja2python
from jinja2python import render_to_response, render_to_string
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

def hello_view(request):
    """ Simple Hello World View """
    t = loader.get_template('helloworld.html')
    c = Context({
        'current_time': datetime.now(),
    })
    return HttpResponse(t.render(c))

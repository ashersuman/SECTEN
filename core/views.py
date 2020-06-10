from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.
class dashboard(TemplateView):
    template_name = 'core/dashboard.html'

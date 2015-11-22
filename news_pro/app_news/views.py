from django.shortcuts import render
from django.views.generic import (View, ListView, DetailView, edit, TemplateView,
                                  CreateView)

# Create your views here.

class Index(TemplateView):
    template_name = 'index  `\ .html'


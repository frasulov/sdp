from django.urls import path
from django.views.generic import TemplateView
from .views import *

urlpatterns = [
    path("", TemplateView.as_view(template_name="ner/index.html"), name="index"),
    path("api/v1/ner", NerProcessView.as_view(), name="ner"),
    path("v2", TemplateView.as_view(template_name="ner/index_v2.html"), name="index_v2"),
    path("about-us", TemplateView.as_view(template_name="ner/about_us.html"), name="about_us"),
]
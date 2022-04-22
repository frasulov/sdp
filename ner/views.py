from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from .serializer import NerInputSeriaziler
# Create your views here.


class NerProcessView(CreateAPIView):
    serializer_class = NerInputSeriaziler
from django.views import View
from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

class Login(View):
    def get(self,request):
        return HttpResponse("Hello, world. You're at the polls index.")
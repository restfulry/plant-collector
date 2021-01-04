from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return HttpResponse('<h1>Hello /ᐠ｡‸｡ᐟ\ﾉ</h1>')


def about(request):
    return render(request, 'about.html')


def plants_index(request):
    return render(request, 'plants/index.html', {'plants': plants})

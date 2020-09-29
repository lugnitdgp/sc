from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    # print('ok')
    # return render(request, 'home.html')
    return HttpResponse('ok')
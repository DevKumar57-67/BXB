from django.shortcuts import render

# Create your views here.
from django.shortcuts import render


def bxb(request):
    return render(request, 'core/bxb.html')
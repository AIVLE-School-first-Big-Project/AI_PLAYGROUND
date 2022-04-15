from django.shortcuts import render

from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils import timezone

from django.core.paginator import Paginator
from django.db.models import Q
# Create your views here.

def first_view(request):
    return render(request, 'ani/first_view.html')

def write(request):
    return render(request, 'ani/write.html')

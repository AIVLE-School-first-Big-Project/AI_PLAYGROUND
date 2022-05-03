from django.shortcuts import redirect, render
from django.http import HttpResponse
import requests
from datetime import datetime, timedelta
# from dotenv import load_dotenv
import os
from django.utils import timezone
from .models import Guest_Book


def index(request):
  guest_book = Guest_Book.objects.all().order_by('-id')
  if request.method == 'POST' and request.POST['content'] != '':
    Guest_Book(region=request.POST.get('region'), content=request.POST.get('content')).save()
  return render(request, 'guest_book/index.html', {'guestbook':guest_book})
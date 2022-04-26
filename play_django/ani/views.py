from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils import timezone

from django.core.paginator import Paginator
from django.db.models import Q

import requests
from .forms import FileUploadForm
from .models import FileUpload
import os
# Create your views here.

def first_view(request):
    return render(request, 'ani/first_view.html')

def write(request):
    return render(request, 'ani/write.html')

def fileUpload(request):
    if request.method == 'POST':
        img = request.FILES['imgfile']
        img.name = '1.jpg'
        fileupload = FileUpload(
            imgfile=img,
        )
        fileupload.save()
        files = open("media/ani_images/"+img.name, 'rb')

        upload = {'file': fileupload.imgfile,
                'filename':fileupload.imgfile.name[11:]
        }
        res = requests.post('http://127.0.0.1:5000/predict', files = upload)
        return render(request, 'ani/result.html', upload)
    else:
        fileuploadForm = FileUploadForm
        context = {
            'fileuploadForm': fileuploadForm,
        }
        return render(request, 'ani/fileupload.html', context)
    
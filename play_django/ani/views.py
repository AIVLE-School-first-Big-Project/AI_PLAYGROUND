from unicodedata import name
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils import timezone

from django.core.paginator import Paginator
from django.db.models import Q

import requests
from .forms import FileUploadForm
from .models import FileUpload
import os
import cv2

from ast import literal_eval
# Create your views here.

def fileUpload(request):
    if request.method == 'POST':
        try:
            img = request.FILES['imgfile']
        except:
            print('no')
            return render(request, 'ani/noface.html')
        img.name = '1.jpg'
        fileupload = FileUpload(
            imgfile=img,
        )
        fileupload.save()
        files = open("media/ani_images/"+img.name, 'rb')
        upload = {'file': fileupload.imgfile,
                'filename':fileupload.imgfile.name[11:]
        }
        res = requests.post('http://127.0.0.1:5001/predict', files = upload)

        test=literal_eval(res.json())
        if test['try'] == 'success':
            return render(request, 'ani/result.html', upload)
        else:
            return render(request, 'ani/noface.html')
        
    else:
        fileuploadForm = FileUploadForm
        context = {
            'fileuploadForm': fileuploadForm,
        }
        return render(request, 'ani/fileupload.html', context)
    
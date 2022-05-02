from django.shortcuts import render,get_object_or_404, redirect
from ast import literal_eval
import requests
import json
from django.http import HttpResponse,JsonResponse
from .forms import pcimgUploadForm
from .models import pcimgUpload
import os
from django.conf import settings
import time
import datetime

def fileUpload(request):
    if request.method == 'POST':
        img = request.FILES["image"]
        ntime = datetime.datetime.now()
        time = datetime.datetime.strftime(ntime, '%Y%m%d%H%M%S')
        img.name=time+'.'+img.name.split('.')[1]
        fileupload = pcimgUpload(
        image=img
        )
        fileupload.save()
        files=open("media/pcolor/"+img.name, 'rb')

        upload = {'file': files,
                'filename':img.name
        }
        res = requests.post('http://127.0.0.1:5000/colorpredict', files = upload)
        test=literal_eval(res.json())
        
        return render(request, 'pcolor/result.html',test)
    else:
        form = pcimgUploadForm()
        context = {
            'fileuploadForm': form,
        }
    return render(request, 'pcolor/phome.html', context)


def download(request):
    if request.method == 'GET':
        pcolor = request.GET.get('pcolor', '')
        filepath = str(settings.BASE_DIR) + ('\\pcolor\\static\\pcolor\\imgs\\%s' % pcolor+".jpg")
        print(filepath)
        filename = os.path.basename(filepath)
        with open(filepath, 'rb') as f:
            response = HttpResponse(f, content_type='application/octet-stream')
            response['Content-Disposition'] = 'attachment; filename=%s' % filename        
    return response


# def share(request):
#     if request.method == 'GET':
#         pcolor = request.GET.get('pcolor', '')
#         context = {
#             'pcolor': pcolor,
#         }       
#     return render(request, 'pcolor/result.html',context)

def share(request):
    if request.method == 'GET':
        pcolor = request.GET.get('pcolor', '')
        context = {
            'pcolor': pcolor,
        }
    return  render(request, 'pcolor/result.html',context)
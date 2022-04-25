from django.shortcuts import render,get_object_or_404, redirect
from ast import literal_eval
import requests
import json
from .forms import pcimgUploadForm
from .models import pcimgUpload

def fileUpload(request):
    if request.method == 'POST':
        img = request.FILES["image"]
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

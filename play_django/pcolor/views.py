from django.shortcuts import render,get_object_or_404, redirect
from ast import literal_eval
import requests
import json
from django.http import HttpResponse,JsonResponse
from .forms import pcimgUploadForm
from .models import pcimgUpload,pcsave
from member.models import User

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

def save(request): 
    if request.is_ajax():
        user_id = request.GET['user_id']
        if not request.user.is_authenticated: 
            message = "로그인이 필요합니다" 
            context = {"message":message} 
            return HttpResponse(json.dumps(context), content_type='application/json')
        user = request.user
        if pcsave.save.filter(id = User.user_id).exists(): 
           pcsave.save.remove(user) 
           message = "저장 취소" 
        else:
            pcsave.save(user_id)
            message = "저장" #화면에 띄울 메세지
        context = {"message":message}
        return HttpResponse(json.dumps(context), content_type='application/json')  
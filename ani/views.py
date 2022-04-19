from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils import timezone

from django.core.paginator import Paginator
from django.db.models import Q

from .forms import FileUploadForm
from .models import FileUpload
# Create your views here.

def first_view(request):
    return render(request, 'ani/first_view.html')

def write(request):
    return render(request, 'ani/write.html')

def fileUpload(request):
    if request.method == 'POST':
        img = request.FILES["imgfile"]
        fileupload = FileUpload(
            imgfile=img,
        )
        fileupload.save()
        return render(request, 'ani/result.html')
    else:
        fileuploadForm = FileUploadForm
        context = {
            'fileuploadForm': fileuploadForm,
        }
        return render(request, 'ani/fileupload.html', context)
    
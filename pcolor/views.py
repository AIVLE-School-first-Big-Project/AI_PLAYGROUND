from django.shortcuts import render,get_object_or_404, redirect

from .forms import pcimgUploadForm
from .models import pcimgUpload

def fileUpload(request):
    if request.method == 'POST':
        img = request.FILES["image"]
        fileupload = pcimgUpload(
            image=img
        )
        fileupload.save()
        return render(request, 'pcolor/result.html')
    else:
        form = pcimgUploadForm()
        context = {
            'fileuploadForm': form,
        }
    return render(request, 'pcolor/phome.html', context)

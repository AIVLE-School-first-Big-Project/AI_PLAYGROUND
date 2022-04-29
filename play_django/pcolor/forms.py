from django.forms import ModelForm
from .models import pcimgUpload,pcsave

class pcimgUploadForm(ModelForm):
    class Meta:
        model = pcimgUpload
        fields = ['image']
        labels = {
            'image':'이미지파일'
        }

class pcresultForm(ModelForm):
    class Meta:
        model=pcsave
        fields=['pcolor']
        labels = {
            'pcolor':'퍼스널컬러',
       }
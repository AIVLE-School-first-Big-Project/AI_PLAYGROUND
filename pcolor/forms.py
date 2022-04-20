from django.forms import ModelForm
from .models import pcimgUpload

class pcimgUploadForm(ModelForm):
    class Meta:
        model = pcimgUpload
        fields = ['image']
        labels = {
            'image':'이미지파일'
        }
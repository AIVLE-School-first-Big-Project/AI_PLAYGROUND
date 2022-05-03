from django import forms
from .models import Board

class BoardForm(forms.ModelForm):
    
    class Meta:
        model = Board
        fields = ['title', 'body', 'file', 'model_name']
        labels = {
            'title': '제목',
            'model_name': '모델명',
            'body': '내용',
            'file':'파일',
        }
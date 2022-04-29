from django import forms
from .models import Board

class BoardForm(forms.ModelForm):
    
    class Meta:
        model = Board
        fields = ['title', 'body', 'file']
        labels = {
            'title': '제목',
            'body': '내용',
            'file':'파일'
        }
from django.db import models
from member.models import User

class pcimgUpload(models.Model):
    image = models.ImageField(upload_to='pcolor/')    
  

class pcsave(models.Model):
    pcolor = models.CharField(max_length=50)

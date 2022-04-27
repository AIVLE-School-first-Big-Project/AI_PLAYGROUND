from django.db import models
from member.models import User

class pcimgUpload(models.Model):
    user_id = models.ForeignKey(  
    User, on_delete = models.SET_NULL, null=True, db_column = 'user_id')
    date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='pcolor/')    
  

class pcsave(models.Model):
    pcolorname = models.CharField(max_length=50)
    resultimage= models.ImageField(upload_to='pcolor/result/')
    class Meta:
        db_table = 'pcsave'
        app_label = 'pcsave'
        managed = False

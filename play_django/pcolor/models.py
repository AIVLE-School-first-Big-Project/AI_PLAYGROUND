from django.db import models

class pcimgUpload(models.Model):
    title = models.CharField(max_length=255,null=False)
    image = models.ImageField(upload_to='pcolor/')
    
    def __str__(self):
        return self.title
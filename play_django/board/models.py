from django.db import models

from member.models import User

class Board(models.Model):
    user_id = models.ForeignKey(  
        User, on_delete = models.SET_NULL, null=True, db_column = 'user_id')
    date = models.DateTimeField()
    model_name = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    body = models.TextField()
    file = models.FileField(upload_to='', blank = True)

    class Meta:
        db_table = 'board'
        app_label = 'board'
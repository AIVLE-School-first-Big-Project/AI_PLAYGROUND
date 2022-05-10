from django.db import models

class User(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=20, unique=True, null=False)
    password = models.CharField(max_length=255, null=False)
    email = models.CharField(max_length=50, unique=True, null=False)
    current_rftoken = models.CharField(max_length=255, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user_id

    # class Meta:
    #     db_table = 'User'
    #     managed = False
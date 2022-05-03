from django.db import models
class Guest_Book(models.Model):
    region = models.CharField(max_length=50, blank=False)
    content = models.TextField(blank=False)

    def __str__(self):
        return self.content
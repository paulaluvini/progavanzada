from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Quota(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    procesados = models.IntegerField(default=0, editable=False)
    disponibles = models.IntegerField()


class EmailHistorico(models.Model):
    text = models.TextField(blank = True)
    created_at = models.DateTimeField(auto_now=True)
    result = models.TextField(blank = True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

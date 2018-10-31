from django.db import models
from django.contrib.auth.models import User

class Trans(models.Model):
    owner = models.ForeignKey(User, on_delete="PROTECT",null = True, blank = True)
    trans_id = models.IntegerField()
    u_id = models.TextField()
    r_id = models.TextField()
     

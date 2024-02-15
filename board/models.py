from django.db import models
from django.contrib.auth.models import User

STATUS = (('1', 'New'), 
          ('2', 'In progress'), 
          ('3', 'In QA'), 
          ('4', 'Ready'), 
          ('5', 'Done'))
# Create your models here.
class Task(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    status = models.CharField(max_length=11, choices=STATUS)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creator')
    assigner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigner', null=True)
    updated_at = models.DateTimeField(auto_now=True)

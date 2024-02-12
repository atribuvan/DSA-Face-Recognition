from django.db import models
import os

def image_upload_path(instance, filename):
    _, ext = os.path.splitext(filename)
    
    return f'app/images/{instance.product_id}{ext}'

class Product(models.Model):
    product_id = models.CharField(max_length=10, primary_key=True,default=1)
    product_name=models.CharField(max_length=25)
    image=models.ImageField(upload_to=image_upload_path)

    def __str__(self):
        return self.product_name

from django.db import models
from django.contrib.auth.models import User

class Attendance(models.Model):
    date = models.DateField()
    student = models.ForeignKey(User, on_delete=models.CASCADE) 
    status = models.CharField(max_length=10, choices=[("Present", "Present"), ("Absent", "Absent")])

    def __str__(self):
        return self.date.strftime('%Y-%m-%d')

    

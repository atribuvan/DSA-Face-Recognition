


import os
import django
from . import settings
# Set the DJANGO_SETTINGS_MODULE
os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings)
django.setup()
from django.contrib.auth.models import User
from datetime import date
from app.models import Attendance

# Import your Django models


# Query the database
results = User.objects.all()
for item in results:
    print(item.username)

# def get_rollnumber(lab):
#     #   print(image_id)
#     # #   imgpath="media/app/images/11.jpg"
#     #   imgpath=f'media/app/images/{image_id}.jpg'
     
#     #   lab=roll(imgpath)
        
#       date = date(2023, 11, 8)
#       context = {
#             'lab':lab,
#             # 'image_id':image_id
#         }
#       for lastname in lab:
#         student = User.objects.get(username=lastname)
#         Attendance.objects.create(date=date, student=student, status="Present")
#     #   return redirect('record_attendance',lab)
#     #   return render(request,'hi.html',context)


# lab={'VarshithCSE-292','mvars','mvars1'}
# get_rollnumber(lab)
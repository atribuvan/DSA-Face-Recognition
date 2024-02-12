from django.shortcuts import render,HttpResponse,redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from . forms import productform
from . import final
from .final import roll
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from datetime import date
from app.models import Attendance
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
import csv
import os
from .models import Product
from datetime import date
from django.http import FileResponse
from django.http import HttpResponse
from django.conf import settings

# Create your views here.


def home(request):
    return render(request,'toot.html')

def upload_photo(request):
    if request.user.is_authenticated:
        form = productform()
        return render(request,'index.html',{'form':form})   
    else:
         return HttpResponseRedirect(reverse("login1"))


def upload(request):
    if request.method=='POST':
        form=productform(request.POST,request.FILES)
        if form.is_valid():
            product =form.save()
            image_id = product.product_id
            return redirect('get_rollnumber',image_id)

        else:
            return  HttpResponse('invalid')
    else:  
        return  HttpResponse('method must be post')  


    

def get_rollnumber(request,image_id):
      print(image_id)
      imgpath=f'media/app/images/{image_id}.jpg'
     
      lab=roll(imgpath)

      context = {
            'lab':lab,
            'image_id':image_id
        }
      date1 = date(2023, 11, 9)
      present_students=[]
      for last1 in lab:
        if len(last1)==2:
            last2='2200010'+last1
            present_students.append(last2)
        
        else : 
            last2='22000100'+last1
            present_students.append(last2)
        try:    
            student = User.objects.get(last_name=last2)
            Attendance.objects.create(date=date1, student=student, status="Present")
        except User.DoesNotExist:
                pass   
    #   print(present_students)  
      update_attendance(image_id,present_students)
      return render(request,'hi.html',context)







def signup(request):
     return render(request, "signup.html")

def register(request):
    if request.method=='POST':

        firstname=request.POST['firstname']
        lastname=request.POST['lastname']
        password=request.POST['password']
        cnfpassword=request.POST['confirmPassword']
        if password != cnfpassword:
            return render(request, "signup.html", {
                "message": "Passwords must match."
            })
        
        try:
           

            user = User.objects.create_user(username=firstname + lastname, password=password)

            user.first_name = firstname
            user.last_name = lastname

            user.save()


        except:
            return render(request, "signup.html", {
                "message": "Username already taken."
            })
        return HttpResponseRedirect(reverse("logged"))
    else:
        return render(request, "flight/register.html")


def logged(request):
    
    if request.method=='POST':
        username=request.POST['name']
        email=request.POST['email']
        password=request.POST['password']
        user_type = request.POST.get('user_type')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            if user_type == 'student':               
                return redirect('studentpage')
            elif user_type == 'teacher':
              return redirect('home')
        else:
           context={'message':'Invalid Credentials'}
           return render(request, "login.html",context) 
        

    else:
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('home'))
        else:

            return render(request, "login.html")    
def login1(request):
     return render(request, "login.html")

from .two import get_first_image_path
def student_page(request):
                last_name = request.user.last_name
                first_name = request.user.first_name
  
                lis=no_of_absentess(last_name)
                b=last_name[-2]
                # b=str(1)
                # print(b)
                # print(type(b))
                if(b=='0'):
                 last_two_characters = last_name[-1:]
                else:
                 last_two_characters = last_name[-2:]
                # print(last_two_characters)
                subfolder_name = last_two_characters 
                # subfolder_name = '1'
                root_folder = 'app\static/training_data'
                file_path = "app\static/training_data/1/1.jpg"

                # index = file_path.find("app\static/\")
                # trimmed_path = file_path.replace("app\\static\\", "")

                # print("Trimmed Path:", trimmed_path)
                imgpath=get_first_image_path(subfolder_name,root_folder)
                imgpath=imgpath[10:]
                # print(imgpath)
                # print(trimmed_path)
                # print(25)
                context = {
                    'last_name': last_name,
                    'last_two_characters':last_two_characters,
                    # 'first_name': "two",
                    'imgpath':imgpath,
                    'first_name': first_name,
                    'lis':lis
                }
                return render(request, 'student.html', context)

def logoutpage(request):
    logout(request)
    return redirect('home')


def hi(request):
    return render(request,'hi.html')







def serve_custom_file(request, filename):
    custom_file_path =  'app\marking.csv'
    
    if os.path.exists(custom_file_path):
        with open(custom_file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/csv')
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response
    else:
        return HttpResponse("File not found", status=404)
    




def download_marking_pdf(request):
    csv_file_path = 'app\marking.csv'

    if not os.path.isfile(csv_file_path):
        return HttpResponse("The marking.csv file does not exist.")

    with open(csv_file_path, 'r') as file:
        csv_data = list(csv.reader(file))

    pdf_file_path = os.path.join(settings.MEDIA_ROOT, 'marking.pdf')
    doc = SimpleDocTemplate(pdf_file_path, pagesize=letter)

    data = []

    for i, row in enumerate(csv_data, start=1):
        row_color = 'lightgrey' if i % 2 == 0 else 'white' 
        data.append([row[0], row[1],row[2]])
    row_color1='lightgrey'
    row_color='white'
    table = Table(data)
    table.setStyle(TableStyle([ ('GRID', (0, 0), (-1, -1), 1, (0, 0, 0)), ('BACKGROUND', (0, 0), (-1, 0), row_color), ('BACKGROUND', (0, 1), (-1, -1), row_color1), ]))


    elements = [table]
    doc.build(elements)

    with open(pdf_file_path, 'rb') as pdf_file:
        response = HttpResponse(pdf_file.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="marking.pdf"'

    return response

def attend(request):
      return  render(request,"attendance_form.html") 

    


from datetime import datetime
def attendance_by_date(request):
    if request.method == 'POST':
        date = request.POST.get('selected_date')
        date = datetime.strptime(date, '%Y-%m-%d').date()
        reverse_date_str = date.strftime('%d-%m-%Y')

        date = str(reverse_date_str)
        try:
            target_column_name = str(date) 
            print(type(target_column_name))

            present_students = []
            absent_students = []
            csv_file='app\output.csv'
            with open(csv_file, 'r') as file:
             
                csv_reader = csv.DictReader(file)

            

                for row in csv_reader:
                    attendance_status = row.get(target_column_name)

                    if attendance_status == '1':
                        roll_number = row['roll_number']
                        present_students.append(roll_number)
                        print(roll_number)
                    else:
                        roll_number = row['roll_number']
                        absent_students.append(roll_number)
                        print(roll_number)
            context = {
                    'selected_date': date,
                    'present_students': present_students,
                    'not_present_users': absent_students,
                }            
            return render(request, 'attendance_by_date.html', context)
        except ValueError:
            error_message = "Invalid date format. Please use 'YYYY-MM-DD'."
            return render(request, 'attendance_form.html', {'error_message': error_message})
    else:
        return render(request, 'attendance_form.html')


def past(request):    
    pass
def add(request):   
    pass
   
import csv
from django.contrib.auth.models import User
from django.http import HttpResponse

def create_users_from_csv(request):
    csv_file_path = 'app/reference.csv'

    try:
        with open(csv_file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                roll_number = row['roll_number']
                name = row['name']
                first_name = name
                last_name = roll_number
                username = first_name + last_name
                password = roll_number

                if not User.objects.filter(username=username).exists():
                    User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name)

        return HttpResponse('User accounts created successfully')
    except Exception as e:
        return HttpResponse(f'Error: {str(e)}')


import csv


def update_attendance(date,present_students):
    

        attendance_file = 'app\output.csv'  
        with open(attendance_file, mode='r', newline='') as file:
            reader = csv.reader(file)
            rows = list(reader)

        header = rows[0]
        header.append(date)

        present_students_set = set(present_students)

        for row in rows[1:]:
            roll_number = row[0]
            if roll_number in present_students_set:
                row.append("1")
            else:
                row.append("0")

        with open(attendance_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows)



   
def no_of_absentess(rollnumber1):
        csv_file = 'app\output.csv'
        desired_roll_number = rollnumber1  

        count_ones = 0
        count=0
        
        lis=[]
        row_data = None

        with open(csv_file, 'r') as file:
            csv_reader = csv.reader(file)
            header = next(csv_reader)  
            count = len(header)-1
            for row in csv_reader:
                roll_number = row[0]  
                if roll_number == desired_roll_number:
                    row_data = row
                    count_ones = sum(int(cell) for cell in row[1:])
                   
        lis.append(count_ones)        
        lis.append(count-count_ones)    
        if count!=0:    
            lis.append((count_ones/count)*100)   
        else :
            lis.append (0)         
        lis.append(count)    
                    
        return lis    





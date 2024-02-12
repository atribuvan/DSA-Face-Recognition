from django.urls import path
from . import views
urlpatterns = [

    path('upload',views.upload,name='upload'),
    path('upload_photo',views.upload_photo,name='upload_photo'),
    path('view_past_attendances',views.past,name='view_past_attendances'),
    path('add_update_student_info',views.add,name='add_update_student_info'),
    path('',views.home,name='home'),
    path('get_rollnumber/<str:image_id>/', views.get_rollnumber, name='get_rollnumber'),
    path('custom_files/<path:filename>/', views.serve_custom_file, name='serve_custom_file'),
    path('download-marking-pdf/', views.download_marking_pdf, name='download_marking_pdf'),
    path('register',views.register,name='register'),
    path('signup',views.signup,name='signup'),
    path('login1',views.login1,name='login1'),
    path('logoutpage',views.logoutpage,name='logout'),
    path('logged',views.logged,name='logged'),
    path('attend',views.attend,name='attend'),
    path('attendance_by_date/', views.attendance_by_date, name='attendance_by_date'),
    path('create_users_from_csv/', views.create_users_from_csv, name='create_users_from_csv'),
    path('update_attendance/', views.update_attendance, name='update_attendance'),
    path('studentpage/', views.student_page, name='studentpage'),

]
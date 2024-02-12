from django.contrib import admin
from . models import Product,Attendance
# Register your models here.
admin.site.register(Attendance)
@admin.register(Product)
class productadmin(admin.ModelAdmin):
    list_display=['product_name','image']

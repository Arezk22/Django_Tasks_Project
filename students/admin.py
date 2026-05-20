from django.contrib import admin
from .models import Student

# Register your models here.
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
  def full_name(self, obj):
    if obj.l_name:
        return f"{obj.f_name} {obj.l_name}"
    return obj.f_name
  full_name.short_description = 'Full Name'

  fields=('f_name','l_name','age','course_name','dept_name')
  list_display=('full_name', 'age' ,'course_name','dept_name' ,'enrolled_at')
  list_filter=('age','dept_name')
  search_fields=('f_name', 'l_name')
  date_hierarchy='enrolled_at'
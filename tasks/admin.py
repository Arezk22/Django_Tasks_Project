from django.contrib import admin
from .models import Task 

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin): 
    fields=('title', 'completed','status','priority')   
    list_display = ('title', 'completed', 'created_at', 'updated_at')
    list_filter = ('completed', 'created_at')
    search_fields = ('title', 'description')
    date_hierarchy = 'created_at'
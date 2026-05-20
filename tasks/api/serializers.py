from rest_framework import serializers
from ..models import Task

class TaskSerializer(serializers.ModelSerializer):

  status_display = serializers.CharField(source='get_status_display', read_only=True)
  priority_display = serializers.CharField(source='get_priority_display', read_only=True)
  owner_display = serializers.CharField(source='user.username', read_only=True)
 



  class Meta:
    model = Task
    fields = ['id', 'title', 'description','status','status_display','priority','priority_display', 'completed','user','owner_display','due_date', 'created_at']
    read_only_fields=['id','user','due_date', 'created_at']
from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    STATUS_CHOISE=[
        ('pending','Pending'),
        ('in_progress','in_Progress'),
        ('done','Done')
    ]
    PRIORITY_CHOISES=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high' , 'High')
    ]
    # user model
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    # (Fields)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    status=models.CharField(max_length=20 , choices=STATUS_CHOISE , default='pending')
    priority=models.CharField(max_length=20 , choices=PRIORITY_CHOISES , default='medium')
    completed = models.BooleanField(default=False)
    due_date = models.DateField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  

    class Meta:              
        ordering = ['created_at']         
  
    def __str__(self):
        return self.title
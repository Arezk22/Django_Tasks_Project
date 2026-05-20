from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

DEPT_CHOISES=[
  ('it','It'),
  ('cs','Cs'),
  ('is','Is')
]
# Create your models here.
class Student(models.Model):
   f_name=models.CharField(max_length=20)
   l_name=models.CharField(max_length=20 ,null=True,blank=True)
   age = models.IntegerField(
    validators=[
        MinValueValidator(18),
        MaxValueValidator(28)
    ]
    )
   course_name = models.CharField(
        max_length=20,
        null=True,
        blank=True
    )
   dept_name = models.CharField(
        max_length=20,
        choices=DEPT_CHOISES
    )
   enrolled_at=models.DateTimeField(auto_now_add=True)

   class Meta:
        ordering = ['enrolled_at']     

   def __str__(self):
         return self.f_name
   
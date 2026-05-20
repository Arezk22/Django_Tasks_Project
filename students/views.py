from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Student
from .forms import StudentForm

# 1. عرض كل الطلاب (Read)
def student_list(request):
    students = Student.objects.all()
    return render(request, 'students/student_list.html', {'students': students})

# 2. إضافة طالب جديد (Create)
def student_create(request):
    form = StudentForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Add Student Successfully')
        return redirect('student_list')
    return render(request, 'students/student_form.html', {'form': form})

# 3. تعديل بيانات طالب (Update)
def student_update(request, pk):
    student = Student.objects.get(id=pk)
    form = StudentForm(request.POST or None, instance=student)
    if form.is_valid():
        form.save()
        messages.info(request, f'update data of {student.f_name} Successfully.')
        return redirect('student_list')
    return render(request, 'students/student_form.html', {'form': form})

# 4. حذف طالب (Delete)
def student_delete(request, pk):
    student = Student.objects.get(id=pk)
    if request.method == 'POST':
        student.delete()
        messages.warning(request, 'student deleted successfully')
        return redirect('student_list')
    return render(request, 'students/student_confirm_delete.html', {'student': student})
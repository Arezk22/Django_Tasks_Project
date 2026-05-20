from django.contrib import messages 
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login 
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from .forms import TaskForm
from .models import Task

def custom_login(request):
    if request.user.is_authenticated:
        return redirect('task_list')    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('task_list')
    else:
        form = AuthenticationForm()    
    return render(request, 'tasks/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('task_list')
    else:
        form = UserCreationForm()    
    return render(request, 'tasks/register.html', {'form': form})

@login_required
def task_list(request):
    
    if request.user.is_staff:
        tasks_queryset = Task.objects.all().select_related('user')
    else:
        tasks_queryset = Task.objects.filter(user=request.user)    
    tasks_by_status = {
        'pending': tasks_queryset.filter(status='pending'),
        'in_progress': tasks_queryset.filter(status='in_progress'),
        'done': tasks_queryset.filter(status='done'),
    }    
    context = {
        'tasks_list': tasks_queryset,  
        'tasks': tasks_by_status,
    }
    return render(request, 'tasks/task_list.html', context)
    


@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user   # ربط المهمة بالمستخدم الحالي
            task.save()
            messages.success(request, "Add task successfully🚀")
            return redirect('task_list')
    else:
        form = TaskForm()    
    return render(request, 'tasks/task_form.html', {'form': form})


@login_required
def task_update(request, pk):
    if request.user.is_staff:
        task = get_object_or_404(Task, pk=pk)
    else:
        task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, "update Task successfully✅")
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)    
    return render(request, 'tasks/task_form.html', {'form': form})


@login_required
def task_detail(request, pk):
    if request.user.is_staff:
        task = get_object_or_404(Task, pk=pk)
    else:
        task = get_object_or_404(Task, pk=pk, user=request.user)
    
    return render(request, 'tasks/task_details.html', {'task': task})


@login_required
def task_delete(request, pk):
    if request.user.is_staff:
        task = get_object_or_404(Task, pk=pk)
    else:
        task = get_object_or_404(Task, pk=pk, user=request.user)    
    if request.method == 'POST':
        task.delete()
        messages.success(request, "Deleted Task Successfully🗑️")
        return redirect('task_list')    
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})
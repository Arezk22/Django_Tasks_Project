from django.urls import path ,include
from django.contrib.auth.views import LogoutView
from .views import custom_login, register , task_list,task_update,task_delete,task_create, task_detail
# from .api.views import tasks_api

urlpatterns = [
    path('',task_list, name='task_list'),
    path('create/', task_create, name='task_create'),
    path('update/<int:pk>/', task_update, name='task_update'),
    path('delete/<int:pk>/', task_delete, name='task_delete'),
    path('details/<int:pk>/', task_detail, name='task_details'),
    path('login/', custom_login, name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', register, name='register'),  
    # path('api/tasks/', tasks_list_api, name='api-tasks-list'),   
    # path('api/v1/', include('tasks.api.urls'))
]
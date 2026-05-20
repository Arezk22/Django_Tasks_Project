from django.urls import path , include
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.decorators import api_view, permission_classes
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'tasks',views.TaskViewSet, basename='task')
urlpatterns = [
    path('tasks/', views.tasks_api, name='tasks-api'),
    path('tasks/<int:pk>/', views.task_detail_api, name='task-detail-api'),
    path('tasks/<int:pk>/', views.TaskApiView.as_view(), name='api_task_detail'),
    path('viewset/', include(router.urls))
]
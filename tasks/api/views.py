from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework import status
from rest_framework.views import APIView
from tasks.api.permissions import IsOwnerOrAdmin
from rest_framework import viewsets,filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.routers import DefaultRouter
from .serializers import TaskSerializer 
from ..models import Task


# function base view
@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def tasks_api(request):
    if request.method == 'GET':
        if request.user.is_staff:
            tasks = Task.objects.all()
        else:
            tasks = Task.objects.filter(user=request.user)        
        if not tasks.exists():
            return Response({"error": "No tasks found"}, status=status.HTTP_404_NOT_FOUND)
        status_param = request.query_params.get('status')
        
        if status_param is not None:
            if status_param == 'pending':
                tasks = tasks.filter(status='pending')
            elif status_param == 'in_progress':
                tasks = tasks.filter(status='in_progress')
            elif status_param == 'done':
                tasks = tasks.filter(status='done')    
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data , status=status.HTTP_200_OK)        

    elif request.method == 'POST':
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data , status=status.HTTP_201_CREATED)
        else: 
            return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT','DELETE','PATCH'])
@permission_classes([IsAuthenticated])
def task_detail_api(request, pk):
    if request.user.is_staff:
        task = Task.objects.filter(pk=pk).first()
    else:
        task = Task.objects.filter(pk=pk , user=request.user).first()
        queryset = Task.objects.filter(user=request.user)
    if not task:
        raise NotFound({"Error":"Task not found"})
    if request.method == 'GET':        
        serializer = TaskSerializer(task , many=False)
        return Response(serializer.data , status=status.HTTP_200_OK)    
    if request.method == 'PUT':
        serializer = TaskSerializer(task , data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
        
    if request.method == 'PATCH':
        serializer = TaskSerializer(task , data = request.data , partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'DELETE':
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
    



# --------class based view-----------------



class TaskApiView(APIView):
    permission_classes = [IsAuthenticated , IsOwnerOrAdmin]  
    def get_object(self,pk):
        task = Task.objects.filter(pk=pk).first()
        if not task:
            raise NotFound({"Error":"Task not found"}) 
        self.check_object_permissions(self.request, task)  # Check permissions for the object
        return task   

    def get(self,request , pk=None):
        if pk:
            task = self.get_object(pk)
            serializer = TaskSerializer(task, many=False)
            return Response(serializer.data , status=status.HTTP_200_OK)
        if request.user.is_staff:
            task = Task.objects.all()  
        else:
            task = Task.objects.filter(user=request.user)
        if not task.exists():
            return Response({"error": "No tasks found"}, status=status.HTTP_404_NOT_FOUND)        
        serializer = TaskSerializer(task , many=True)
        return Response(serializer.data , status=status.HTTP_200_OK)
    
    def post(self,request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data , status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
        
    def put(self,request,pk):
        task = self.get_object(self,pk)
        serializer = TaskSerializer(task,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status=status.HTTP_200_OK)
        else: 
            return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)

    def patch(self,request,pk):
        task = self.get_object(self,pk)
        serializer = TaskSerializer(task,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status=status.HTTP_200_OK)
        else: 
            return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self,pk):
        task = self.get_object(self,pk)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        

# ViewSets and routers                 
class TaskViewSet(viewsets.ModelViewSet):
    # queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    filter_backends = [
        DjangoFilterBackend, 
        filters.SearchFilter, 
        filters.OrderingFilter 
    ]
    filterset_fields = ['completed', 'priority']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'due_date']
    def get_queryset(self):
        if self.request.user.is_staff:
            return Task.objects.all()
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action (detail=False , methods = ['GET'])
    def summary(self, request):
        
        if request.user.is_staff:
            total_tasks= Task.objects.count()
            completed_tasks = Task.objects.filter(completed=True).count()
            pending_tasks=Task.objects.filter(status='pending').count()
            in_progress_tasks=Task.objects.filter(status='in_progress').count()
            done_tasks=Task.objects.filter(status='done').count()
        else:
            total_tasks= Task.objects.filter(user=request.user).count()
            completed_tasks = Task.objects.filter(user=request.user, completed=True).count()
            pending_tasks=Task.objects.filter(user=request.user,status='pending').count()
            in_progress_tasks=Task.objects.filter(user=request.user,status='in_progress').count()
            done_tasks=Task.objects.filter(user=request.user,status='done').count()
        data = {
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'pending_tasks': pending_tasks,
            'in_progress_tasks': in_progress_tasks,
            'done_tasks': done_tasks
        }
        return Response(data)
    
    @action(detail=True,methods=['POST'])
    def mark_status(self,request,pk=None):
          if request.user.is_staff:
            task = Task.objects.filter(pk=pk).first()
            if not task:
                raise NotFound({"Error":"Task not found"})
          else:
            task = Task.objects.filter(pk=pk,user=request.user).first()
            if not task:
                raise NotFound({"Error":"Task not found"})
          status_param = request.data.get('status')
          if status_param not in ['pending', 'in_progress', 'done']:
              return Response({"error": "Invalid status value"}, status=status.HTTP_400_BAD_REQUEST)
          task.status = status_param
          task.save()
          serializer = TaskSerializer(task)
          return Response(serializer.data , status=status.HTTP_200_OK)
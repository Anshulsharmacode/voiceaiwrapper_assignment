from django.urls import path
from .views import (
    TaskListView,
    TaskDetailView,
    ProjectTaskListView
)

app_name = 'task'

urlpatterns = [
    # List all tasks or create a new one
    path('', TaskListView.as_view(), name='list-create'),
    
    # Get, update, or delete a specific task by ID
    path('<int:task_id>/', TaskDetailView.as_view(), name='detail'),
    
    # List all tasks for a specific project
    path('project/<int:project_id>/', ProjectTaskListView.as_view(), name='by-project'),
]

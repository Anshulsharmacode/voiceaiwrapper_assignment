from django.urls import path
from .views import (
    TaskCommentListView,
    TaskCommentDetailView,
    TaskCommentsListView
)

app_name = 'taskcomment'

urlpatterns = [
    # List all comments or create a new one
    path('', TaskCommentListView.as_view(), name='list-create'),
    
    # Get, update, or delete a specific comment by ID
    path('<int:comment_id>/', TaskCommentDetailView.as_view(), name='detail'),
    
    # List all comments for a specific task
    path('task/<int:task_id>/', TaskCommentsListView.as_view(), name='by-task'),
]


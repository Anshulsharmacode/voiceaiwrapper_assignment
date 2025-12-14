from django.urls import path
from .views import (
    ProjectListView,
    ProjectDetailView,
    OrganizationProjectListView
)

app_name = 'project'

urlpatterns = [
    # List all projects or create a new one
    path('', ProjectListView.as_view(), name='list-create'),
    
    # Get, update, or delete a specific project by ID
    path('<int:project_id>/', ProjectDetailView.as_view(), name='detail'),
    
    # List all projects for a specific organization
    path('organization/<int:org_id>/', OrganizationProjectListView.as_view(), name='by-organization'),
]

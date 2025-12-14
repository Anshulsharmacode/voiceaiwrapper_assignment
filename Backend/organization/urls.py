from django.urls import path
from .views import (
    OrganizationListView,
    OrganizationDetailView,
    OrganizationBySlugView
)

app_name = 'organization'

urlpatterns = [
    # List all organizations or create a new one
    path('', OrganizationListView.as_view(), name='list-create'),
    
    # Get organization by slug
    path('slug/<str:slug>/', OrganizationBySlugView.as_view(), name='by-slug'),
    
    # Get, update, or delete a specific organization by ID
    path('<int:org_id>/', OrganizationDetailView.as_view(), name='detail'),
]

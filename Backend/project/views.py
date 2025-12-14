import json
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.exceptions import ValidationError
from .service import ProjectService
from .serializers import ProjectSerializer


@method_decorator(csrf_exempt, name='dispatch')
class ProjectListView(View):
    """View for listing all projects and creating new projects."""

    def get(self, request):
        """
        List all projects.
        """
        try:
            search_query = request.GET.get('search', '').strip()
            status = request.GET.get('status', '').strip()
            organization_id = request.GET.get('organization_id', '').strip()
            
            if search_query:
                org_id = int(organization_id) if organization_id else None
                projects = ProjectService.search_projects(search_query, organization_id=org_id)
            elif status:
                org_id = int(organization_id) if organization_id else None
                projects = ProjectService.filter_projects_by_status(status, organization_id=org_id)
            elif organization_id:
                projects = ProjectService.get_projects_by_organization(int(organization_id))
            else:
                projects = ProjectService.get_all_projects()
            
            data = ProjectSerializer.to_list_dict(projects)
            
            return JsonResponse({
                'success': True,
                'data': data,
                'count': len(data)
            }, status=200)
        
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)

    def post(self, request):
        """Create a new project."""
        try:
            try:
                body_data = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({
                    'success': False,
                    'error': 'Invalid JSON in request body.'
                }, status=400)
            
            validated_data = ProjectSerializer.validate_create_data(body_data)
            
            project = ProjectService.create_project(**validated_data)
            
            return JsonResponse({
                'success': True,
                'data': ProjectSerializer.to_dict(project),
                'message': 'Project created successfully.'
            }, status=201)
        
        except ValidationError as e:
            return JsonResponse({
                'success': False,
                'error': 'Validation failed.',
                'errors': e.message_dict if hasattr(e, 'message_dict') else {'detail': str(e)}
            }, status=400)
        
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class ProjectDetailView(View):
    """View for retrieving, updating, and deleting a specific project."""

    def get(self, request, project_id):
        """Retrieve a specific project by ID."""
        try:
            project = ProjectService.get_project_by_id(project_id)
            
            if not project:
                return JsonResponse({
                    'success': False,
                    'error': 'Project not found.'
                }, status=404)
            
            return JsonResponse({
                'success': True,
                'data': ProjectSerializer.to_dict(project)
            }, status=200)
        
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)

    def put(self, request, project_id):
        """Update a project (full update)."""
        return self._update(request, project_id, partial=False)

    def patch(self, request, project_id):
        """Update a project (partial update)."""
        return self._update(request, project_id, partial=True)

    def _update(self, request, project_id, partial=False):
        """Internal method to handle update operations."""
        try:
            project = ProjectService.get_project_by_id(project_id)
            
            if not project:
                return JsonResponse({
                    'success': False,
                    'error': 'Project not found.'
                }, status=404)
            
            try:
                body_data = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({
                    'success': False,
                    'error': 'Invalid JSON in request body.'
                }, status=400)
            
            if not partial:
              
                validated_data = ProjectSerializer.validate_create_data(body_data)
            else:
                validated_data = ProjectSerializer.validate_update_data(body_data)
            
            updated_project = ProjectService.update_project(project_id, **validated_data)
            
            if not updated_project:
                return JsonResponse({
                    'success': False,
                    'error': 'Project not found.'
                }, status=404)
            
            return JsonResponse({
                'success': True,
                'data': ProjectSerializer.to_dict(updated_project),
                'message': 'Project updated successfully.'
            }, status=200)
        
        except ValidationError as e:
            return JsonResponse({
                'success': False,
                'error': 'Validation failed.',
                'errors': e.message_dict if hasattr(e, 'message_dict') else {'detail': str(e)}
            }, status=400)
        
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)

    def delete(self, request, project_id):
        """Delete a project."""
        try:
            deleted = ProjectService.delete_project(project_id)
            
            if not deleted:
                return JsonResponse({
                    'success': False,
                    'error': 'Project not found.'
                }, status=404)
            
            return JsonResponse({
                'success': True,
                'message': 'Project deleted successfully.'
            }, status=200)
        
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class OrganizationProjectListView(View):
    """View for listing all projects for a specific organization."""

    def get(self, request, org_id):
        """
        List all projects for a specific organization.
        """
        try:
            search_query = request.GET.get('search', '').strip()
            status = request.GET.get('status', '').strip()
            
            if search_query:
                projects = ProjectService.search_projects(search_query, organization_id=org_id)
            elif status:
                projects = ProjectService.filter_projects_by_status(status, organization_id=org_id)
            else:
                projects = ProjectService.get_projects_by_organization(org_id)
            
            data = ProjectSerializer.to_list_dict(projects)
            
            return JsonResponse({
                'success': True,
                'data': data,
                'count': len(data)
            }, status=200)
        
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)

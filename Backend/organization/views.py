import json
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.exceptions import ValidationError
from .service import OrganizationService
from .serializers import OrganizationSerializer


@method_decorator(csrf_exempt, name='dispatch')
class OrganizationListView(View):
  

    def get(self, request):
        """
        List all organizations.
        
        Query parameters:
            - search: Optional search query to filter organizations
        """
        try:
            search_query = request.GET.get('search', '').strip()
            
            if search_query:
                organizations = OrganizationService.search_organizations(search_query)
            else:
                organizations = OrganizationService.get_all_organizations()
            
            data = OrganizationSerializer.to_list_dict(organizations)
            
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
        """Create a new organization."""
        try:
         
            try:
                body_data = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({
                    'success': False,
                    'error': 'Invalid JSON in request body.'
                }, status=400)
            
           
            validated_data = OrganizationSerializer.validate_create_data(body_data)
            
            
            organization = OrganizationService.create_organization(**validated_data)
            
            
            return JsonResponse({
                'success': True,
                'data': OrganizationSerializer.to_dict(organization),
                'message': 'Organization created successfully.'
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
class OrganizationDetailView(View):
    """View for retrieving, updating, and deleting a specific organization."""

    def get(self, request, org_id):
        """Retrieve a specific organization by ID."""
        try:
            organization = OrganizationService.get_organization_by_id(org_id)
            
            if not organization:
                return JsonResponse({
                    'success': False,
                    'error': 'Organization not found.'
                }, status=404)
            
            return JsonResponse({
                'success': True,
                'data': OrganizationSerializer.to_dict(organization)
            }, status=200)
        
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)

    def put(self, request, org_id):
        """Update an organization (full update)."""
        return self._update(request, org_id, partial=False)

    def patch(self, request, org_id):
        """Update an organization (partial update)."""
        return self._update(request, org_id, partial=True)

    def _update(self, request, org_id, partial=False):
        """Internal method to handle update operations."""
        try:
          
            if not OrganizationService.organization_exists(org_id):
                return JsonResponse({
                    'success': False,
                    'error': 'Organization not found.'
                }, status=404)
            
         
            try:
                body_data = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({
                    'success': False,
                    'error': 'Invalid JSON in request body.'
                }, status=400)
            
           
            validated_data = OrganizationSerializer.validate_update_data(body_data)
            
            if not validated_data:
                return JsonResponse({
                    'success': False,
                    'error': 'No valid fields provided for update.'
                }, status=400)
            
       
            organization = OrganizationService.update_organization(org_id, **validated_data)
            
            if not organization:
                return JsonResponse({
                    'success': False,
                    'error': 'Organization not found.'
                }, status=404)
            
         
            return JsonResponse({
                'success': True,
                'data': OrganizationSerializer.to_dict(organization),
                'message': 'Organization updated successfully.'
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

    def delete(self, request, org_id):
        """Delete an organization."""
        try:
            deleted = OrganizationService.delete_organization(org_id)
            
            if not deleted:
                return JsonResponse({
                    'success': False,
                    'error': 'Organization not found.'
                }, status=404)
            
            return JsonResponse({
                'success': True,
                'message': 'Organization deleted successfully.'
            }, status=200)
        
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class OrganizationBySlugView(View):
    """View for retrieving an organization by slug."""

    def get(self, request, slug):
        """Retrieve an organization by slug."""
        try:
            organization = OrganizationService.get_organization_by_slug(slug)
            
            if not organization:
                return JsonResponse({
                    'success': False,
                    'error': 'Organization not found.'
                }, status=404)
            
            return JsonResponse({
                'success': True,
                'data': OrganizationSerializer.to_dict(organization)
            }, status=200)
        
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)

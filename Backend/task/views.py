import json
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.exceptions import ValidationError
from .service import TaskService
from .serializers import TaskSerializer


@method_decorator(csrf_exempt, name='dispatch')
class TaskListView(View):
    """View for listing all tasks and creating new tasks."""

    def get(self, request):
        """
        List all tasks.
        """
        try:
            project_id = request.GET.get('project_id', '').strip()
            
            if project_id:
                tasks = TaskService.get_tasks_by_project(int(project_id))
            else:
                tasks = TaskService.get_all_tasks()
            
            data = TaskSerializer.to_list_dict(tasks)
            
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
        """Create a new task."""
        try:
            try:
                body_data = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({
                    'success': False,
                    'error': 'Invalid JSON in request body.'
                }, status=400)
            
            validated_data = TaskSerializer.validate_create_data(body_data)
            
            task = TaskService.create_task(**validated_data)
            
            return JsonResponse({
                'success': True,
                'data': TaskSerializer.to_dict(task),
                'message': 'Task created successfully.'
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
class TaskDetailView(View):
    """View for retrieving, updating, and deleting a specific task."""

    def get(self, request, task_id):
        """Retrieve a specific task by ID."""
        try:
            task = TaskService.get_task_by_id(task_id)
            
            if not task:
                return JsonResponse({
                    'success': False,
                    'error': 'Task not found.'
                }, status=404)
            
            return JsonResponse({
                'success': True,
                'data': TaskSerializer.to_dict(task)
            }, status=200)
        
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)

    def put(self, request, task_id):
        """Update a task (full update)."""
        return self._update(request, task_id, partial=False)

    def patch(self, request, task_id):
        """Update a task (partial update)."""
        return self._update(request, task_id, partial=True)

    def _update(self, request, task_id, partial=False):
        """Internal method to handle update operations."""
        try:
            task = TaskService.get_task_by_id(task_id)
            
            if not task:
                return JsonResponse({
                    'success': False,
                    'error': 'Task not found.'
                }, status=404)
            
            try:
                body_data = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({
                    'success': False,
                    'error': 'Invalid JSON in request body.'
                }, status=400)
            
            if not partial:
                validated_data = TaskSerializer.validate_create_data(body_data)
            else:
                validated_data = TaskSerializer.validate_update_data(body_data)
            
            updated_task = TaskService.update_task(task_id, **validated_data)
            
            if not updated_task:
                return JsonResponse({
                    'success': False,
                    'error': 'Task not found.'
                }, status=404)
            
            return JsonResponse({
                'success': True,
                'data': TaskSerializer.to_dict(updated_task),
                'message': 'Task updated successfully.'
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

    def delete(self, request, task_id):
        """Delete a task."""
        try:
            deleted = TaskService.delete_task(task_id)
            
            if not deleted:
                return JsonResponse({
                    'success': False,
                    'error': 'Task not found.'
                }, status=404)
            
            return JsonResponse({
                'success': True,
                'message': 'Task deleted successfully.'
            }, status=200)
        
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class ProjectTaskListView(View):
    """View for listing all tasks for a specific project."""

    def get(self, request, project_id):
        """
        List all tasks for a specific project.
        """
        try:
            tasks = TaskService.get_tasks_by_project(project_id)
            
            data = TaskSerializer.to_list_dict(tasks)
            
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

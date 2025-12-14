import json
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.exceptions import ValidationError
from .service import TaskCommentService
from .serializers import TaskCommentSerializer


@method_decorator(csrf_exempt, name='dispatch')
class TaskCommentListView(View):
    """View for listing all comments and creating new comments."""

    def get(self, request):
        """
        List all comments.
        """
        try:
            task_id = request.GET.get('task_id', '').strip()
            
            if task_id:
                comments = TaskCommentService.get_comments_by_task(int(task_id))
            else:
                comments = TaskCommentService.get_all_comments()
            
            data = TaskCommentSerializer.to_list_dict(comments)
            
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
        """Create a new comment."""
        try:
            try:
                body_data = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({
                    'success': False,
                    'error': 'Invalid JSON in request body.'
                }, status=400)
            
            validated_data = TaskCommentSerializer.validate_create_data(body_data)
            
            comment = TaskCommentService.create_comment(**validated_data)
            
            return JsonResponse({
                'success': True,
                'data': TaskCommentSerializer.to_dict(comment),
                'message': 'Comment created successfully.'
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
class TaskCommentDetailView(View):
    """View for retrieving, updating, and deleting a specific comment."""

    def get(self, request, comment_id):
        """Retrieve a specific comment by ID."""
        try:
            comment = TaskCommentService.get_comment_by_id(comment_id)
            
            if not comment:
                return JsonResponse({
                    'success': False,
                    'error': 'Comment not found.'
                }, status=404)
            
            return JsonResponse({
                'success': True,
                'data': TaskCommentSerializer.to_dict(comment)
            }, status=200)
        
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)

    def put(self, request, comment_id):
        """Update a comment (full update)."""
        return self._update(request, comment_id, partial=False)

    def patch(self, request, comment_id):
        """Update a comment (partial update)."""
        return self._update(request, comment_id, partial=True)

    def _update(self, request, comment_id, partial=False):
        """Internal method to handle update operations."""
        try:
            comment = TaskCommentService.get_comment_by_id(comment_id)
            
            if not comment:
                return JsonResponse({
                    'success': False,
                    'error': 'Comment not found.'
                }, status=404)
            
            try:
                body_data = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({
                    'success': False,
                    'error': 'Invalid JSON in request body.'
                }, status=400)
            
            if not partial:
                validated_data = TaskCommentSerializer.validate_create_data(body_data)
            else:
                validated_data = TaskCommentSerializer.validate_update_data(body_data)
            
            updated_comment = TaskCommentService.update_comment(comment_id, **validated_data)
            
            if not updated_comment:
                return JsonResponse({
                    'success': False,
                    'error': 'Comment not found.'
                }, status=404)
            
            return JsonResponse({
                'success': True,
                'data': TaskCommentSerializer.to_dict(updated_comment),
                'message': 'Comment updated successfully.'
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

    def delete(self, request, comment_id):
        """Delete a comment."""
        try:
            deleted = TaskCommentService.delete_comment(comment_id)
            
            if not deleted:
                return JsonResponse({
                    'success': False,
                    'error': 'Comment not found.'
                }, status=404)
            
            return JsonResponse({
                'success': True,
                'message': 'Comment deleted successfully.'
            }, status=200)
        
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class TaskCommentsListView(View):
    """View for listing all comments for a specific task."""

    def get(self, request, task_id):
        """
        List all comments for a specific task.
        """
        try:
            comments = TaskCommentService.get_comments_by_task(task_id)
            
            data = TaskCommentSerializer.to_list_dict(comments)
            
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

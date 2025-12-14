from typing import Dict, Any, Optional
from django.core.exceptions import ValidationError
from .models import TaskComment


class TaskCommentSerializer:
    """Serializer for TaskComment model."""

    @staticmethod
    def validate_create_data(data: Dict[str, Any]) -> Dict[str, Any]:
        errors = {}
        
        task_id = data.get('task_id')
        if not task_id:
            errors['task_id'] = 'Task ID is required.'
        elif not isinstance(task_id, int):
            try:
                task_id = int(task_id)
            except (ValueError, TypeError):
                errors['task_id'] = 'Task ID must be a valid integer.'
        
        content = data.get('content', '').strip()
        if not content:
            errors['content'] = 'Content is required.'
        
        author_email = data.get('author_email', '').strip()
        if not author_email:
            errors['author_email'] = 'Author email is required.'
        elif '@' not in author_email:
            errors['author_email'] = 'Author email must be a valid email address.'
        
        if errors:
            raise ValidationError(errors)
        
        cleaned_data = {
            'task_id': task_id,
            'content': content,
            'author_email': author_email,
        }
        
        return cleaned_data

    @staticmethod
    def validate_update_data(data: Dict[str, Any]) -> Dict[str, Any]:
        errors = {}
        cleaned_data = {}
        
        if 'task_id' in data:
            task_id = data.get('task_id')
            if not isinstance(task_id, int):
                try:
                    task_id = int(task_id)
                except (ValueError, TypeError):
                    errors['task_id'] = 'Task ID must be a valid integer.'
            if 'task_id' not in errors:
                cleaned_data['task_id'] = task_id
        
        if 'content' in data:
            content = data.get('content', '').strip()
            if not content:
                errors['content'] = 'Content cannot be empty.'
            else:
                cleaned_data['content'] = content
        
        if 'author_email' in data:
            author_email = data.get('author_email', '').strip()
            if not author_email:
                errors['author_email'] = 'Author email cannot be empty.'
            elif '@' not in author_email:
                errors['author_email'] = 'Author email must be a valid email address.'
            else:
                cleaned_data['author_email'] = author_email
        
        if errors:
            raise ValidationError(errors)
        
        return cleaned_data

    @staticmethod
    def to_dict(comment: TaskComment) -> Dict[str, Any]:
        """
        Convert TaskComment instance to dictionary.
        """
        return {
            'id': comment.id,
            'task_id': comment.task.id,
            'content': comment.content,
            'author_email': comment.author_email,
            'timestamp': comment.timestamp.isoformat() if comment.timestamp else None
        }

    @staticmethod
    def to_list_dict(comments: list[TaskComment]) -> list[Dict[str, Any]]:
        return [TaskCommentSerializer.to_dict(comment) for comment in comments]

from typing import Dict, Any, Optional
from django.core.exceptions import ValidationError
from .models import Task, TASK_STATUS_CHOICES


class TaskSerializer:
    """Serializer for Task model."""

    @staticmethod
    def validate_create_data(data: Dict[str, Any]) -> Dict[str, Any]:
        errors = {}
        
        project_id = data.get('project_id')
        if not project_id:
            errors['project_id'] = 'Project ID is required.'
        elif not isinstance(project_id, int):
            try:
                project_id = int(project_id)
            except (ValueError, TypeError):
                errors['project_id'] = 'Project ID must be a valid integer.'
        
        title = data.get('title', '').strip()
        if not title:
            errors['title'] = 'Title is required.'
        
        status = data.get('status', '').strip()
        if not status:
            errors['status'] = 'Status is required.'
        elif status not in [choice[0] for choice in TASK_STATUS_CHOICES]:
            errors['status'] = f'Status must be one of: {", ".join([choice[0] for choice in TASK_STATUS_CHOICES])}.'
        
        description = data.get('description', '').strip()
        assignee_email = data.get('assignee_email', '').strip()
        due_date = data.get('due_date')
        
        if errors:
            raise ValidationError(errors)
        
        cleaned_data = {
            'project_id': project_id,
            'title': title,
            'status': status,
            'description': description,
            'assignee_email': assignee_email,
        }
        
        if due_date:
            cleaned_data['due_date'] = due_date
        
        return cleaned_data

    @staticmethod
    def validate_update_data(data: Dict[str, Any]) -> Dict[str, Any]:
        errors = {}
        cleaned_data = {}
        
        if 'project_id' in data:
            project_id = data.get('project_id')
            if not isinstance(project_id, int):
                try:
                    project_id = int(project_id)
                except (ValueError, TypeError):
                    errors['project_id'] = 'Project ID must be a valid integer.'
            if 'project_id' not in errors:
                cleaned_data['project_id'] = project_id
        
        if 'title' in data:
            title = data.get('title', '').strip()
            if not title:
                errors['title'] = 'Title cannot be empty.'
            else:
                cleaned_data['title'] = title
        
        if 'status' in data:
            status = data.get('status', '').strip()
            if not status:
                errors['status'] = 'Status cannot be empty.'
            elif status not in [choice[0] for choice in TASK_STATUS_CHOICES]:
                errors['status'] = f'Status must be one of: {", ".join([choice[0] for choice in TASK_STATUS_CHOICES])}.'
            else:
                cleaned_data['status'] = status
        
        if 'description' in data:
            cleaned_data['description'] = data.get('description', '').strip()
        
        if 'assignee_email' in data:
            cleaned_data['assignee_email'] = data.get('assignee_email', '').strip()
        
        if 'due_date' in data:
            due_date = data.get('due_date')
            if due_date is not None:
                cleaned_data['due_date'] = due_date
            else:
                cleaned_data['due_date'] = None
        
        if errors:
            raise ValidationError(errors)
        
        return cleaned_data

    @staticmethod
    def to_dict(task: Task) -> Dict[str, Any]:
        """
        Convert Task instance to dictionary.
        """
        return {
            'id': task.id,
            'project_id': task.project.id,
            'title': task.title,
            'description': task.description,
            'status': task.status,
            'assignee_email': task.assignee_email,
            'due_date': task.due_date.isoformat() if task.due_date else None,
            'created_at': task.created_at.isoformat() if task.created_at else None
        }

    @staticmethod
    def to_list_dict(tasks: list[Task]) -> list[Dict[str, Any]]:
        return [TaskSerializer.to_dict(task) for task in tasks]

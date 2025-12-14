from typing import Dict, Any, Optional
from django.core.exceptions import ValidationError
from .models import Project, STATUS_CHOICES


class ProjectSerializer:
    """Serializer for Project model."""

    @staticmethod
    def validate_create_data(data: Dict[str, Any]) -> Dict[str, Any]:
       
        errors = {}
        
        organization_id = data.get('organization_id')
        if not organization_id:
            errors['organization_id'] = 'Organization ID is required.'
        elif not isinstance(organization_id, int):
            try:
                organization_id = int(organization_id)
            except (ValueError, TypeError):
                errors['organization_id'] = 'Organization ID must be a valid integer.'
        
        name = data.get('name', '').strip()
        if not name:
            errors['name'] = 'Name is required.'
        
        status = data.get('status', '').strip()
        if not status:
            errors['status'] = 'Status is required.'
        elif status not in [choice[0] for choice in STATUS_CHOICES]:
            errors['status'] = f'Status must be one of: {", ".join([choice[0] for choice in STATUS_CHOICES])}.'
        
        description = data.get('description', '').strip()
        due_date = data.get('due_date')
        
        if errors:
            raise ValidationError(errors)
        
        cleaned_data = {
            'organization_id': organization_id,
            'name': name,
            'status': status,
            'description': description,
        }
        
        if due_date:
            cleaned_data['due_date'] = due_date
        
        return cleaned_data

    @staticmethod
    def validate_update_data(data: Dict[str, Any]) -> Dict[str, Any]:
      
        errors = {}
        cleaned_data = {}
        
        if 'organization_id' in data:
            organization_id = data.get('organization_id')
            if not isinstance(organization_id, int):
                try:
                    organization_id = int(organization_id)
                except (ValueError, TypeError):
                    errors['organization_id'] = 'Organization ID must be a valid integer.'
            if 'organization_id' not in errors:
                cleaned_data['organization_id'] = organization_id
        
        if 'name' in data:
            name = data.get('name', '').strip()
            if not name:
                errors['name'] = 'Name cannot be empty.'
            else:
                cleaned_data['name'] = name
        
        if 'status' in data:
            status = data.get('status', '').strip()
            if not status:
                errors['status'] = 'Status cannot be empty.'
            elif status not in [choice[0] for choice in STATUS_CHOICES]:
                errors['status'] = f'Status must be one of: {", ".join([choice[0] for choice in STATUS_CHOICES])}.'
            else:
                cleaned_data['status'] = status
        
        if 'description' in data:
            cleaned_data['description'] = data.get('description', '').strip()
        
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
    def to_dict(project: Project) -> Dict[str, Any]:
        """
        Convert Project instance to dictionary.
       
        """
        return {
            'id': project.id,
            'organization_id': project.organization.id,
            'name': project.name,
            'description': project.description,
            'status': project.status,
            'due_date': project.due_date.isoformat() if project.due_date else None,
            'created_at': project.created_at.isoformat() if project.created_at else None
        }

    @staticmethod
    def to_list_dict(projects: list[Project]) -> list[Dict[str, Any]]:
    
        return [ProjectSerializer.to_dict(project) for project in projects]

from typing import Dict, Any
from django.core.exceptions import ValidationError
from .models import Organization
from slugify import slugify

class OrganizationSerializer:
    """Serializer for Organization model."""

    @staticmethod
    def validate_create_data(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Clean and prepare data for creating an organization.
        Model validation (max_length, email format, etc.) is handled by Django model fields.
        
        Args:
            data: Dictionary containing organization data
            
        Returns:
            Cleaned data dictionary
            
        Raises:
            ValidationError: If required fields are missing
        """
        errors = {}
        
        name = data.get('name', '').strip()
        if not name:
            errors['name'] = 'Name is required.'
        
        contact_email = data.get('contact_email', '').strip()
        if not contact_email:
            errors['contact_email'] = 'Contact email is required.'
        
        if errors:
            raise ValidationError(errors)
        
        slug = data.get('slug', '').strip()
        if not slug:
            slug = slugify(name)
        
        return {
            'name': name,   
            'slug': slug if slug else None,
            'contact_email': contact_email
        }

    @staticmethod
    def validate_update_data(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Clean and prepare data for updating an organization.
        Model validation (max_length, email format, etc.) is handled by Django model fields.
        
        Args:
            data: Dictionary containing organization data to update
            
        Returns:
            Cleaned data dictionary with only provided fields
            
        Raises:
            ValidationError: If provided fields are empty
        """
        errors = {}
        cleaned_data = {}
        
        if 'name' in data:
            name = data.get('name', '').strip()
            if not name:
                errors['name'] = 'Name cannot be empty.'
            else:
                cleaned_data['name'] = name
        
        if 'slug' in data:
            slug = data.get('slug', '').strip()
            if slug: 
                cleaned_data['slug'] = slug
            else:
                cleaned_data['slug'] = slugify(name)
        
        if 'contact_email' in data:
            contact_email = data.get('contact_email', '').strip()
            if not contact_email:
                errors['contact_email'] = 'Contact email cannot be empty.'
            else:
                cleaned_data['contact_email'] = contact_email
        
        if errors:
            raise ValidationError(errors)
        
        return cleaned_data

    @staticmethod
    def to_dict(organization: Organization) -> Dict[str, Any]:
        """
        Convert Organization instance to dictionary.
        
        Args:
            organization: Organization instance
            
        Returns:
            Dictionary representation of the organization
        """
        return {
            'id': organization.id,
            'name': organization.name,
            'slug': organization.slug,
            'contact_email': organization.contact_email,
            'created_at': organization.created_at.isoformat() if organization.created_at else None
        }

    @staticmethod
    def to_list_dict(organizations: list[Organization]) -> list[Dict[str, Any]]:
        """
        Convert list of Organization instances to list of dictionaries.
        
        Args:
            organizations: List of Organization instances
            
        Returns:
            List of dictionary representations
        """
        return [OrganizationSerializer.to_dict(org) for org in organizations]

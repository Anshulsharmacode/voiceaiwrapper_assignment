from typing import Optional, Dict, Any
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from .models import Organization


class OrganizationService:
    """Service class for Organization database operations."""

    @staticmethod
    def create_organization(name: str, slug: Optional[str] = None, contact_email: str = None) -> Organization:
        """
        Create a new organization.
        
        Args:
            name: Organization name
            slug: Optional slug (auto-generated from name if not provided)
            contact_email: Contact email address
            
        Returns:
            Created Organization instance
            
        Raises:
            ValidationError: If validation fails
            IntegrityError: If slug already exists
        """
        try:
            organization = Organization(
                name=name,
                slug=slug,
                contact_email=contact_email
            )
            organization.full_clean()
            organization.save()
            return organization
        except IntegrityError as e:
            if 'slug' in str(e):
                raise ValidationError(f"Organization with slug '{slug or name}' already exists.")
            raise
        except ValidationError:
            raise

    @staticmethod
    def get_organization_by_id(org_id: int) -> Optional[Organization]:
        """
        Retrieve an organization by ID.
        
        Args:
            org_id: Organization ID
            
        Returns:
            Organization instance or None if not found
        """
        try:
            return Organization.objects.get(id=org_id)
        except Organization.DoesNotExist:
            return None

    @staticmethod
    def get_organization_by_slug(slug: str) -> Optional[Organization]:
        """
        Retrieve an organization by slug.
        
        Args:
            slug: Organization slug
            
        Returns:
            Organization instance or None if not found
        """
        try:
            return Organization.objects.get(slug=slug)
        except Organization.DoesNotExist:
            return None

    @staticmethod
    def get_all_organizations() -> list[Organization]:
        """
        Retrieve all organizations.
        
        Returns:
            List of Organization instances
        """
        return list(Organization.objects.all())

    @staticmethod
    def update_organization(org_id: int, **kwargs) -> Optional[Organization]:
        """
        Update an organization.
        
        Args:
            org_id: Organization ID
            **kwargs: Fields to update (name, slug, contact_email)
            
        Returns:
            Updated Organization instance or None if not found
            
        Raises:
            ValidationError: If validation fails
            IntegrityError: If slug already exists
        """
        organization = OrganizationService.get_organization_by_id(org_id)
        if not organization:
            return None

        try:
            for field, value in kwargs.items():
                if hasattr(organization, field) and value is not None:
                    setattr(organization, field, value)
            
            organization.full_clean()
            organization.save()
            return organization
        except IntegrityError as e:
            if 'slug' in str(e):
                raise ValidationError(f"Organization with slug '{kwargs.get('slug')}' already exists.")
            raise
        except ValidationError:
            raise

    @staticmethod
    def delete_organization(org_id: int) -> bool:
        """
        Delete an organization.
        
        Args:
            org_id: Organization ID
            
        Returns:
            True if deleted, False if not found
        """
        organization = OrganizationService.get_organization_by_id(org_id)
        if not organization:
            return False
        
        organization.delete()
        return True

    @staticmethod
    def organization_exists(org_id: int) -> bool:
        """
        Check if an organization exists.
        
        Args:
            org_id: Organization ID
            
        Returns:
            True if exists, False otherwise
        """
        return Organization.objects.filter(id=org_id).exists()

    @staticmethod
    def search_organizations(query: str) -> list[Organization]:
        """
        Search organizations by name, slug, or email.
        
        Args:
            query: Search query string
            
        Returns:
            List of matching Organization instances
        """
        return list(Organization.objects.filter(
            name__icontains=query
        ) | Organization.objects.filter(
            slug__icontains=query
        ) | Organization.objects.filter(
            contact_email__icontains=query
        ).distinct())

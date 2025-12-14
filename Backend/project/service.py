from typing import Optional
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from .models import Project
from organization.models import Organization


class ProjectService:


    @staticmethod
    def create_project(
        organization_id: int,
        name: str,
        status: str,
        description: str = "",
        due_date: Optional[str] = None
    ) -> Project:
        """
        Create a new project.
        
        """
        try:
        
            organization = Organization.objects.get(id=organization_id)
            
            project = Project(
                organization=organization,
                name=name,
                description=description,
                status=status,
                due_date=due_date
            )
            project.full_clean()
            project.save()
            return project
        except Organization.DoesNotExist:
            raise ValidationError(f"Organization with ID {organization_id} does not exist.")
        except IntegrityError as e:
            raise ValidationError(f"Error creating project: {str(e)}")
        except ValidationError:
            raise

    @staticmethod
    def get_project_by_id(project_id: int) -> Optional[Project]:
        """
        Retrieve a project by ID.
        """
        try:
            return Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return None

    @staticmethod
    def get_all_projects() -> list[Project]:
        """
        Retrieve all projects.
        """
        return list(Project.objects.all())

    @staticmethod
    def get_projects_by_organization(organization_id: int) -> list[Project]:
        """
        Retrieve all projects for a specific organization.
        """
        return list(Project.objects.filter(organization_id=organization_id))

    @staticmethod
    def update_project(project_id: int, **kwargs) -> Optional[Project]:
        """
        Update a project.
        """
        project = ProjectService.get_project_by_id(project_id)
        if not project:
            return None

        try:
            # Handle organization_id separately if provided
            if 'organization_id' in kwargs:
                org_id = kwargs.pop('organization_id')
                try:
                    organization = Organization.objects.get(id=org_id)
                    project.organization = organization
                except Organization.DoesNotExist:
                    raise ValidationError(f"Organization with ID {org_id} does not exist.")
            
            # Update other fields
            for field, value in kwargs.items():
                if hasattr(project, field) and value is not None:
                    setattr(project, field, value)
            
            project.full_clean()
            project.save()
            return project
        except IntegrityError as e:
            raise ValidationError(f"Error updating project: {str(e)}")
        except ValidationError:
            raise

    @staticmethod
    def delete_project(project_id: int) -> bool:
        """
        Delete a project.
        
        """
        project = ProjectService.get_project_by_id(project_id)
        if not project:
            return False
        
        project.delete()
        return True

    @staticmethod
    def project_exists(project_id: int) -> bool:
        """
        Check if a project exists
        """
        return Project.objects.filter(id=project_id).exists()

    @staticmethod
    def search_projects(query: str, organization_id: Optional[int] = None) -> list[Project]:
        """
        Search projects by name or description.
        
        """
        queryset = Project.objects.filter(
            name__icontains=query
        ) | Project.objects.filter(
            description__icontains=query
        )
        
        if organization_id:
            queryset = queryset.filter(organization_id=organization_id)
        
        return list(queryset.distinct())

    @staticmethod
    def filter_projects_by_status(status: str, organization_id: Optional[int] = None) -> list[Project]:
        """
        Filter projects by status.
        
      
        """
        queryset = Project.objects.filter(status=status)
        
        if organization_id:
            queryset = queryset.filter(organization_id=organization_id)
        
        return list(queryset)

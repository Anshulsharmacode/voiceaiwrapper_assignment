from typing import Optional
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from .models import Task
from project.models import Project


class TaskService:

    @staticmethod
    def create_task(
        project_id: int,
        title: str,
        status: str,
        description: str = "",
        assignee_email: str = "",
        due_date: Optional[str] = None
    ) -> Task:
        """
        Create a new task.
        """
        try:
            project = Project.objects.get(id=project_id)
            
            task = Task(
                project=project,
                title=title,
                description=description,
                status=status,
                assignee_email=assignee_email,
                due_date=due_date
            )
            task.full_clean()
            task.save()
            return task
        except Project.DoesNotExist:
            raise ValidationError(f"Project with ID {project_id} does not exist.")
        except IntegrityError as e:
            raise ValidationError(f"Error creating task: {str(e)}")
        except ValidationError:
            raise

    @staticmethod
    def get_task_by_id(task_id: int) -> Optional[Task]:
        """
        Retrieve a task by ID.
        """
        try:
            return Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return None

    @staticmethod
    def get_all_tasks() -> list[Task]:
        """
        Retrieve all tasks.
        """
        return list(Task.objects.all())

    @staticmethod
    def get_tasks_by_project(project_id: int) -> list[Task]:
        """
        Retrieve all tasks for a specific project.
        """
        return list(Task.objects.filter(project_id=project_id))

    @staticmethod
    def update_task(task_id: int, **kwargs) -> Optional[Task]:
        """
        Update a task.
        """
        task = TaskService.get_task_by_id(task_id)
        if not task:
            return None

        try:
           
            if 'project_id' in kwargs:
                proj_id = kwargs.pop('project_id')
                try:
                    project = Project.objects.get(id=proj_id)
                    task.project = project
                except Project.DoesNotExist:
                    raise ValidationError(f"Project with ID {proj_id} does not exist.")
            
        
            for field, value in kwargs.items():
                if hasattr(task, field) and value is not None:
                    setattr(task, field, value)
            
            task.full_clean()
            task.save()
            return task
        except IntegrityError as e:
            raise ValidationError(f"Error updating task: {str(e)}")
        except ValidationError:
            raise

    @staticmethod
    def delete_task(task_id: int) -> bool:
        """
        Delete a task.
        """
        task = TaskService.get_task_by_id(task_id)
        if not task:
            return False
        
        task.delete()
        return True

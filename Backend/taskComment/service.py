from typing import Optional
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from .models import TaskComment
from task.models import Task


class TaskCommentService:

    @staticmethod
    def create_comment(
        task_id: int,
        content: str,
        author_email: str
    ) -> TaskComment:
        """
        Create a new task comment.
        """
        try:
            task = Task.objects.get(id=task_id)
            
            comment = TaskComment(
                task=task,
                content=content,
                author_email=author_email
            )
            comment.full_clean()
            comment.save()
            return comment
        except Task.DoesNotExist:
            raise ValidationError(f"Task with ID {task_id} does not exist.")
        except IntegrityError as e:
            raise ValidationError(f"Error creating comment: {str(e)}")
        except ValidationError:
            raise

    @staticmethod
    def get_comment_by_id(comment_id: int) -> Optional[TaskComment]:
        """
        Retrieve a comment by ID.
        """
        try:
            return TaskComment.objects.get(id=comment_id)
        except TaskComment.DoesNotExist:
            return None

    @staticmethod
    def get_all_comments() -> list[TaskComment]:
        """
        Retrieve all comments.
        """
        return list(TaskComment.objects.all())

    @staticmethod
    def get_comments_by_task(task_id: int) -> list[TaskComment]:
        """
        Retrieve all comments for a specific task.
        """
        return list(TaskComment.objects.filter(task_id=task_id))

    @staticmethod
    def update_comment(comment_id: int, **kwargs) -> Optional[TaskComment]:
        """
        Update a comment.
        """
        comment = TaskCommentService.get_comment_by_id(comment_id)
        if not comment:
            return None

        try:
            if 'task_id' in kwargs:
                task_id = kwargs.pop('task_id')
                try:
                    task = Task.objects.get(id=task_id)
                    comment.task = task
                except Task.DoesNotExist:
                    raise ValidationError(f"Task with ID {task_id} does not exist.")
            
            for field, value in kwargs.items():
                if hasattr(comment, field) and value is not None:
                    setattr(comment, field, value)
            
            comment.full_clean()
            comment.save()
            return comment
        except IntegrityError as e:
            raise ValidationError(f"Error updating comment: {str(e)}")
        except ValidationError:
            raise

    @staticmethod
    def delete_comment(comment_id: int) -> bool:
        """
        Delete a comment.
        """
        comment = TaskCommentService.get_comment_by_id(comment_id)
        if not comment:
            return False
        
        comment.delete()
        return True


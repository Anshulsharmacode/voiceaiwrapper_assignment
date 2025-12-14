import graphene
from graphene_django import DjangoObjectType
from django.db.models import Count, Q
from datetime import datetime

from organization.models import Organization
from project.models import Project
from task.models import Task
from taskComment.models import TaskComment
from project.service import ProjectService
from task.service import TaskService
from taskComment.service import TaskCommentService


# Type Definitions
class OrganizationType(DjangoObjectType):
    class Meta:
        model = Organization
        fields = ("id", "name", "slug", "contact_email", "created_at")


class ProjectType(DjangoObjectType):
    task_count = graphene.Int()
    completed_task_count = graphene.Int()
    completion_rate = graphene.Float()
    
    class Meta:
        model = Project
        fields = ("id", "organization", "name", "description", "status", "due_date", "created_at")
    
    def resolve_task_count(self, info):
        """Calculate total number of tasks for this project."""
        return self.task_set.count()
    
    def resolve_completed_task_count(self, info):
        """Calculate number of completed tasks."""
        return self.task_set.filter(status='done').count()
    
    def resolve_completion_rate(self, info):
        """Calculate completion rate as a percentage."""
        total = self.task_set.count()
        if total == 0:
            return 0.0
        completed = self.task_set.filter(status='done').count()
        return round((completed / total) * 100, 2)


class TaskType(DjangoObjectType):
    comment_count = graphene.Int()
    
    class Meta:
        model = Task
        fields = ("id", "project", "title", "description", "status", "assignee_email", "due_date", "created_at")
    
    def resolve_comment_count(self, info):
        """Calculate number of comments for this task."""
        return self.comments.count()


class TaskCommentType(DjangoObjectType):
    class Meta:
        model = TaskComment
        fields = ("id", "task", "content", "author_email", "timestamp")


# Input Types for Mutations
class ProjectInput(graphene.InputObjectType):
    organization_id = graphene.Int(required=True)
    name = graphene.String(required=True)
    description = graphene.String()
    status = graphene.String(required=True)
    due_date = graphene.Date()


class ProjectUpdateInput(graphene.InputObjectType):
    name = graphene.String()
    description = graphene.String()
    status = graphene.String()
    due_date = graphene.Date()
    organization_id = graphene.Int()


class TaskInput(graphene.InputObjectType):
    project_id = graphene.Int(required=True)
    title = graphene.String(required=True)
    description = graphene.String()
    status = graphene.String(required=True)
    assignee_email = graphene.String()
    due_date = graphene.DateTime()


class TaskUpdateInput(graphene.InputObjectType):
    title = graphene.String()
    description = graphene.String()
    status = graphene.String()
    assignee_email = graphene.String()
    due_date = graphene.DateTime()
    project_id = graphene.Int()


class TaskCommentInput(graphene.InputObjectType):
    task_id = graphene.Int(required=True)
    content = graphene.String(required=True)
    author_email = graphene.String(required=True)


# Project Statistics Type
class ProjectStatisticsType(graphene.ObjectType):
    total_projects = graphene.Int()
    active_projects = graphene.Int()
    completed_projects = graphene.Int()
    on_hold_projects = graphene.Int()
    total_tasks = graphene.Int()
    completed_tasks = graphene.Int()
    in_progress_tasks = graphene.Int()
    todo_tasks = graphene.Int()
    overall_completion_rate = graphene.Float()


# Queries
class Query(graphene.ObjectType):
    # List projects for an organization
    projects_by_organization = graphene.List(
        ProjectType,
        organization_id=graphene.Int(required=True),
        description="List all projects for a specific organization"
    )
    
    # Project statistics
    project_statistics = graphene.Field(
        ProjectStatisticsType,
        organization_id=graphene.Int(required=True),
        description="Get project statistics for an organization"
    )
    
    # Single project by ID
    project = graphene.Field(
        ProjectType,
        project_id=graphene.Int(required=True),
        description="Get a single project by ID"
    )
    
    # Single task by ID
    task = graphene.Field(
        TaskType,
        task_id=graphene.Int(required=True),
        description="Get a single task by ID"
    )
    
    def resolve_projects_by_organization(self, info, organization_id):
        """Resolve projects for an organization."""
        try:
            projects = ProjectService.get_projects_by_organization(organization_id)
            return projects
        except Exception as e:
            raise Exception(f"Error fetching projects: {str(e)}")
    
    def resolve_project_statistics(self, info, organization_id):
        """Resolve project statistics for an organization."""
        try:
            projects = ProjectService.get_projects_by_organization(organization_id)
            
            total_projects = len(projects)
            active_projects = sum(1 for p in projects if p.status == 'active')
            completed_projects = sum(1 for p in projects if p.status == 'completed')
            on_hold_projects = sum(1 for p in projects if p.status == 'on_hold')
            
            # Get all tasks for these projects
            project_ids = [p.id for p in projects]
            tasks = Task.objects.filter(project_id__in=project_ids)
            
            total_tasks = tasks.count()
            completed_tasks = tasks.filter(status='done').count()
            in_progress_tasks = tasks.filter(status='in_progress').count()
            todo_tasks = tasks.filter(status='todo').count()
            
            overall_completion_rate = 0.0
            if total_tasks > 0:
                overall_completion_rate = round((completed_tasks / total_tasks) * 100, 2)
            
            return ProjectStatisticsType(
                total_projects=total_projects,
                active_projects=active_projects,
                completed_projects=completed_projects,
                on_hold_projects=on_hold_projects,
                total_tasks=total_tasks,
                completed_tasks=completed_tasks,
                in_progress_tasks=in_progress_tasks,
                todo_tasks=todo_tasks,
                overall_completion_rate=overall_completion_rate
            )
        except Exception as e:
            raise Exception(f"Error fetching statistics: {str(e)}")
    
    def resolve_project(self, info, project_id):
        """Resolve a single project by ID."""
        try:
            project = ProjectService.get_project_by_id(project_id)
            if not project:
                raise Exception(f"Project with ID {project_id} not found")
            return project
        except Exception as e:
            raise Exception(f"Error fetching project: {str(e)}")
    
    def resolve_task(self, info, task_id):
        """Resolve a single task by ID."""
        try:
            task = TaskService.get_task_by_id(task_id)
            if not task:
                raise Exception(f"Task with ID {task_id} not found")
            return task
        except Exception as e:
            raise Exception(f"Error fetching task: {str(e)}")


# Mutations
class CreateProject(graphene.Mutation):
    class Arguments:
        input = ProjectInput(required=True)
    
    project = graphene.Field(ProjectType)
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)
    
    def mutate(self, info, input):
        try:
            project = ProjectService.create_project(
                organization_id=input.organization_id,
                name=input.name,
                status=input.status,
                description=input.description or "",
                due_date=input.due_date.isoformat() if hasattr(input.due_date, 'isoformat') else str(input.due_date) if input.due_date else None
            )
            return CreateProject(project=project, success=True, errors=[])
        except Exception as e:
            return CreateProject(project=None, success=False, errors=[str(e)])


class UpdateProject(graphene.Mutation):
    class Arguments:
        project_id = graphene.Int(required=True)
        input = ProjectUpdateInput(required=True)
    
    project = graphene.Field(ProjectType)
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)
    
    def mutate(self, info, project_id, input):
        try:
            update_data = {}
            if input.name is not None:
                update_data['name'] = input.name
            if input.description is not None:
                update_data['description'] = input.description
            if input.status is not None:
                update_data['status'] = input.status
            if input.due_date is not None:
                update_data['due_date'] = input.due_date.isoformat() if hasattr(input.due_date, 'isoformat') else str(input.due_date)
            if input.organization_id is not None:
                update_data['organization_id'] = input.organization_id
            
            project = ProjectService.update_project(project_id, **update_data)
            if not project:
                return UpdateProject(project=None, success=False, errors=[f"Project with ID {project_id} not found"])
            
            return UpdateProject(project=project, success=True, errors=[])
        except Exception as e:
            return UpdateProject(project=None, success=False, errors=[str(e)])


class CreateTask(graphene.Mutation):
    class Arguments:
        input = TaskInput(required=True)
    
    task = graphene.Field(TaskType)
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)
    
    def mutate(self, info, input):
        try:
            task = TaskService.create_task(
                project_id=input.project_id,
                title=input.title,
                status=input.status,
                description=input.description or "",
                assignee_email=input.assignee_email or "",
                due_date=input.due_date.isoformat() if hasattr(input.due_date, 'isoformat') else str(input.due_date) if input.due_date else None
            )
            return CreateTask(task=task, success=True, errors=[])
        except Exception as e:
            return CreateTask(task=None, success=False, errors=[str(e)])


class UpdateTask(graphene.Mutation):
    class Arguments:
        task_id = graphene.Int(required=True)
        input = TaskUpdateInput(required=True)
    
    task = graphene.Field(TaskType)
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)
    
    def mutate(self, info, task_id, input):
        try:
            update_data = {}
            if input.title is not None:
                update_data['title'] = input.title
            if input.description is not None:
                update_data['description'] = input.description
            if input.status is not None:
                update_data['status'] = input.status
            if input.assignee_email is not None:
                update_data['assignee_email'] = input.assignee_email
            if input.due_date is not None:
                update_data['due_date'] = input.due_date.isoformat() if hasattr(input.due_date, 'isoformat') else str(input.due_date)
            if input.project_id is not None:
                update_data['project_id'] = input.project_id
            
            task = TaskService.update_task(task_id, **update_data)
            if not task:
                return UpdateTask(task=None, success=False, errors=[f"Task with ID {task_id} not found"])
            
            return UpdateTask(task=task, success=True, errors=[])
        except Exception as e:
            return UpdateTask(task=None, success=False, errors=[str(e)])


class AddTaskComment(graphene.Mutation):
    class Arguments:
        input = TaskCommentInput(required=True)
    
    comment = graphene.Field(TaskCommentType)
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)
    
    def mutate(self, info, input):
        try:
            comment = TaskCommentService.create_comment(
                task_id=input.task_id,
                content=input.content,
                author_email=input.author_email
            )
            return AddTaskComment(comment=comment, success=True, errors=[])
        except Exception as e:
            return AddTaskComment(comment=None, success=False, errors=[str(e)])


class Mutation(graphene.ObjectType):
    create_project = CreateProject.Field()
    update_project = UpdateProject.Field()
    create_task = CreateTask.Field()
    update_task = UpdateTask.Field()
    add_task_comment = AddTaskComment.Field()


# Root Schema
schema = graphene.Schema(query=Query, mutation=Mutation)


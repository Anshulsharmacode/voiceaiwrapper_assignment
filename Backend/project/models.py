from django.db import models
from organization.models import Organization



STATUS_CHOICES = [
    ('active', 'ACTIVE'),
    ('completed', 'COMPLETED'),
    ('on_hold', 'ON_HOLD'),
  
]


class Project(models.Model):
    """
    Represents a project within an organization.
    Each project belongs to a single organization.
    """
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'
        indexes = [
            models.Index(fields=['organization', '-created_at']),
        ]

    def __str__(self):
        return f"{self.name} ({self.organization.name})"

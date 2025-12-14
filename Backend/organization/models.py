from django.db import models
from django.utils.text import slugify


class Organization(models.Model):
    """
    Represents a tenant in the system.
    Acts as the top-level data boundary for multi-tenancy.
    Owns projects and all related data.
    """
    name = models.CharField(max_length=100)
    slug = models.SlugField( unique=True, db_index=True)
    contact_email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Organization'
        verbose_name_plural = 'Organizations'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

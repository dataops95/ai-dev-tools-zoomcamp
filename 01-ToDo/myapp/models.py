from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Task(models.Model):
    """
    Model representing a single TODO task.
    
    Attributes:
        title: The title/name of the task
        description: Detailed description of the task (optional)
        completed: Boolean flag indicating if task is done
        created_at: Timestamp when task was created
        updated_at: Timestamp when task was last modified
        due_date: Optional deadline for the task
        priority: Priority level of the task
        user: Foreign key to User (optional, for multi-user support)
    """
    
    # Priority choices
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    
    # Core fields
    title = models.CharField(
        max_length=200,
        help_text="Title of the task"
    )
    
    description = models.TextField(
        blank=True,
        null=True,
        help_text="Detailed description of the task"
    )
    
    completed = models.BooleanField(
        default=False,
        help_text="Whether the task is completed"
    )
    
    # Timestamps
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When the task was created"
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="When the task was last updated"
    )
    
    # Optional fields
    due_date = models.DateTimeField(
        blank=True,
        null=True,
        help_text="Deadline for the task"
    )
    
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='medium',
        help_text="Priority level of the task"
    )
    
    # Multi-user support (optional)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tasks',
        blank=True,
        null=True,
        help_text="User who owns this task"
    )
    
    class Meta:
        """Metadata for the Task model."""
        ordering = ['-created_at']  # Newest first
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
    
    def __str__(self) -> str:
        """String representation of the task."""
        return self.title
    
    def is_overdue(self) -> bool:
        """Check if the task is overdue."""
        if self.due_date and not self.completed:
            return timezone.now() > self.due_date
        return False

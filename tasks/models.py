from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
    )

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    class Status(models.TextChoices):
        TODO = 'TODO', 'Todo'
        DOING = 'DOING', 'Doing'
        DONE = 'DONE', 'Done'

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.TODO
    )

    class Priority(models.TextChoices):
        LOW = 'LOW', 'Low'
        MEDIUM = 'MEDIUM', 'Medium'
        HIGH = 'HIGH', 'High'
    
    priority = models.CharField(
        max_length=10,
        choices=Priority.choices, 
        default=Priority.MEDIUM
    )

    due_date = models.DateField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# Create your models here.

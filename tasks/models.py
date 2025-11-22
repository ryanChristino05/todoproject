from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q
# Create your models here.
class Task(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Faible'),
        ('medium', 'Moyenne'),
        ('high', 'Haute'),
    ]
    
    STATUS_CHOICES = [
        ('todo', 'À faire'),
        ('in_progress', 'En cours'),
        ('completed', 'Terminé'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100, verbose_name="Titre")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    completed = models.BooleanField(default=False, verbose_name="Completé")
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField(null=True, blank=True, verbose_name="Date d'échéance")
    
    # Nouveaux champs
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='medium',
        verbose_name="Priorité"
    )
    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='todo',
        verbose_name="Statut"
    )
    
    def __str__(self):
        status_icon = "✅" if self.status == 'completed' else "⏳"
        return f"{status_icon} {self.title}"
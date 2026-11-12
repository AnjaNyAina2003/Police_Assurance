from django.db import models
from django.contrib.auth.models import AbstractUser

from agence_app.models import Agence_assurance

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Administrateur'),
        ('user', 'Utilisateur'),
    )
    
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=50, unique=True)
    agence = models.ForeignKey(Agence_assurance, on_delete=models.SET_NULL, null=True)
    photo = models.ImageField(upload_to='user_photos/', null=True, blank=True)
    
    role = models.CharField(max_length=5, choices=ROLE_CHOICES, default='user')
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS  = ['username']

    def save(self, *args, **kwargs) :
        if self.is_superuser:
            self.role = 'admin'
        super().save(*args, **kwargs)
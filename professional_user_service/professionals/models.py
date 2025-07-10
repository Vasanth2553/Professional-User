from django.db import models

class ProfessionalUser(models.Model):
    user_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    service = models.CharField(max_length=255)
    experience = models.PositiveIntegerField()
    projects = models.TextField()
    skills = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

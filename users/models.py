from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('job_seeker', 'Job Seeker'),
        ('recruiter', 'Recruiter'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='job_seeker')
    skills = models.TextField(blank=True, help_text="Comma-separated skills e.g. Python, Django, SQL")
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"{self.username} ({self.role})"

    def is_recruiter(self):
        return self.role == 'recruiter'

    def is_job_seeker(self):
        return self.role == 'job_seeker'

    def get_skills_list(self):
        """Returns skills as a cleaned list"""
        if self.skills:
            return [s.strip().lower() for s in self.skills.split(',') if s.strip()]
        return []
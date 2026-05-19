from django.db import models
from users.models import CustomUser
from jobs.models import Job

class Application(models.Model):
    STATUS_CHOICES = (
        ('Applied', 'Applied'),
        ('Selected', 'Selected'),
        ('Rejected', 'Rejected'),
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='applications')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Applied')
    cover_letter = models.TextField(blank=True)
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'job')  # Prevent duplicate applications

    def __str__(self):
        return f"{self.user.username} → {self.job.title} [{self.status}]"

    def get_resume_score(self):
        """Simple resume score based on skill matching"""
        return self.job.calculate_match_score(self.user)
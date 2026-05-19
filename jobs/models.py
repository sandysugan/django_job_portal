from django.db import models
from users.models import CustomUser

class Job(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    salary = models.CharField(max_length=100, blank=True)
    required_skills = models.TextField(
        blank=True,
        help_text="Comma-separated required skills e.g. Python, Django, SQL"
    )
    created_by = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='jobs'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} at {self.company}"

    def get_required_skills_list(self):
        if self.required_skills:
            return [s.strip().lower() for s in self.required_skills.split(',') if s.strip()]
        return []

    def calculate_match_score(self, user):
        """Calculate skill match % between job and user"""
        job_skills = set(self.get_required_skills_list())
        user_skills = set(user.get_skills_list())
        if not job_skills:
            return 0
        matched = job_skills.intersection(user_skills)
        score = round((len(matched) / len(job_skills)) * 100)
        return score, list(matched), list(job_skills - user_skills)
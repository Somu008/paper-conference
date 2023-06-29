from django.db import models
from django.contrib.auth.models import User

class ReviewerProfile(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    state = models.CharField(max_length=10, default="draft", choices=(
        ("draft", "draft"),
        ("pending", "pending"),
        ("accepted", "accepted"),
        ("rejected", "rejected")
    ))
    profession = models.CharField(max_length=50, null=True, blank=True)
    institute = models.CharField(max_length=100, null=True, blank=True)
    qualification = models.CharField(max_length=50, null=True, blank=True)
    domain = models.CharField(max_length=30, null=True, blank=True)
    resume = models.FileField(upload_to="resumes", null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.user.username}'s profile"

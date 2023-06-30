from django.db import models
from django.contrib.auth.models import User

from paper.models import Domain

class ReviewerProfile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    state = models.CharField(max_length=10, default="draft", choices=(
        ("draft", "draft"),
        ("pending", "pending"),
        ("accepted", "accepted"),
        ("rejected", "rejected")
    ))
    profession = models.CharField(max_length=50, null=True, blank=True, default="")
    institute = models.CharField(max_length=100, null=True, blank=True, default="")
    qualification = models.CharField(max_length=50, null=True, blank=True, default="")
    resume = models.FileField(upload_to="resumes", null=True, blank=True)
    domains = models.ManyToManyField(Domain, related_name='domains')

    def __str__(self) -> str:
        return f"{self.user.username}'s profile"

from django.db import models
from django.conf import settings



class Domain(models.Model):
    short_name = models.CharField(max_length=20)
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return self.short_name


class Paper(models.Model):
    name = models.CharField(max_length=20,null=True)
    author_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    authors = models.TextField(null=True, blank=True)
    mentor = models.CharField(max_length=20,null=True)
    institute = models.CharField(max_length=20,null=True)
    paper = models.FileField(null=True, upload_to="papers")
    status=models.CharField(default="pending", max_length=20, choices=(
        ("pending", "pending"),
        ("approved", "approved"),
        ("rejected", "rejected")
    ))
    reviewer_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name="reviewer")
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"Paper {self.pk} by {self.name}"

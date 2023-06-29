from django.db import models
from django.contrib.auth.models import User

class ReviewerProfile(models.Model):
    user_id = models.ForeignKey(to=User, on_delete=models.CASCADE)

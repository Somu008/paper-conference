from django.contrib import admin
from .models import Domain, Paper

# Register your models here.

admin.site.register(Paper)
admin.site.register(Domain)

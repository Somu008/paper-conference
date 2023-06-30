from django.contrib import admin
from .models import Domain, Paper

# Register your models here.

class PaperAdmin(admin.ModelAdmin):
    list_display = ['author_id', 'status', 'reviewer_id', 'domain']
    list_filter = ['status', 'reviewer_id', 'institute', 'domain']

admin.site.register(Paper, PaperAdmin)
admin.site.register(Domain)

from django.contrib import admin, auth
from django.contrib.auth import admin as authAdmin

from authentication.models import ReviewerProfile


class ReviewerAdmin(admin.ModelAdmin):
    list_display = ['user', 'state']
    list_filter = ['domains', 'state']

    search_fields = ['user__first_name']

admin.site.register(ReviewerProfile, ReviewerAdmin)

from django.contrib import admin

from . import models

@admin.register(models.Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "repo",
        "owner",
        "stars",
        "open_issues",
        "open_pulls",
        "contributors"
    )

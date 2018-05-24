from django.contrib import admin

from . import models

@admin.register(models.GithubProject)
class GithubProjectAdmin(admin.ModelAdmin):
    list_display = (
        "repo",
        "owner",
        "stars",
        "open_issues",
        "open_pulls",
        "contributors"
    )

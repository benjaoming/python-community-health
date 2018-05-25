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
    list_filter = (
        "ignore",
    )

@admin.register(models.Scoring)
class ScoringAdmin(admin.ModelAdmin):

    list_display = (
        "project",
        "popularity",
        "open_issues",
        "open_pulls",
    )
    list_filter = (
        "project__ignore",
    )

    def open_issues(self, instance):
        return instance.open_issues

    def open_pulls(self, instance):
        return instance.open_issues

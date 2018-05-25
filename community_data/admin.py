from django.contrib import admin

from . import models

@admin.register(models.Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "contributors",
        "stars",
        "open_issues",
        "closed_issues",
        "open_pulls",
        "closed_pulls",
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
        "popularity_vs_contributors",
        "popularity_vs_issues",
        "closed_issues_per_day",
        "days_since_last_pr_merge",
        "popularity_vs_days_since_last_pr_merge",
    )
    # list_filter = (
    #     "project__ignore",
    # )

    def open_issues(self, instance):
        return instance.open_issues

    def open_pulls(self, instance):
        return instance.open_issues

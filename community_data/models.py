from django.db import models


class Project(models.Model):
    
    owner = models.SlugField()
    repo = models.SlugField()
    stars = models.PositiveSmallIntegerField()
    watchers = models.PositiveSmallIntegerField()
    contributors = models.PositiveSmallIntegerField()
    forks = models.PositiveSmallIntegerField()

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    
    open_pulls = models.PositiveSmallIntegerField()
    closed_pulls = models.PositiveSmallIntegerField()
    
    open_issues = models.PositiveSmallIntegerField()
    closed_issues = models.PositiveSmallIntegerField()
    
    last_pr_closed = models.DateTimeField(null=True)
    last_pr_opened = models.DateTimeField(null=True)
    last_issue_closed = models.DateTimeField(null=True)
    
    sync_created = models.DateTimeField(auto_now_add=True)
    sync_last_updated = models.DateTimeField(auto_now=True)

    # Ignores a package in the lists
    ignore = models.BooleanField(default=False)

    class Meta:
        unique_together = ('owner', 'repo')


class Scoring(models.Model):
    """
    In order to keep this simple for a prototype, we just calculate whatever
    metrics we have and save them here.
    
    That way, we can track the development of a project over time and easily
    display and filter metrics in the django admin.
    """
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    open_pulls = models.PositiveSmallIntegerField()
    closed_pulls = models.PositiveSmallIntegerField()
    
    open_issues = models.PositiveSmallIntegerField()
    closed_issues = models.PositiveSmallIntegerField()
    
    #: Aggregated popularity: Watches, stars, forks
    popularity = models.FloatField()

    popularity_vs_issues = models.FloatField()
    
    popularity_vs_contributors = models.FloatField()

    closed_issues_per_day = models.FloatField()

    popularity_vs_closed_issues_per_day = models.FloatField()

    days_since_last_pr_merge = models.FloatField()

    popularity_vs_days_since_last_pr_merge = models.FloatField()

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

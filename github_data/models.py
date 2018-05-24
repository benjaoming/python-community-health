from django.db import models


class GithubProject(models.Model):
    
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

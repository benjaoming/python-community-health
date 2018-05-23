from django.db import models


class GithubProject(models.Model):
    
    owner = models.SlugField()
    repo = models.SlugField()
    stars = models.PositiveSmallIntegerField()
    watchers = models.PositiveSmallIntegerField()
    contributors = models.PositiveSmallIntegerField()
    
    open_pr_count = models.PositiveSmallIntegerField()
    open_issue_count = models.PositiveSmallIntegerField()
    
    last_pr_closed = models.DateTimeField()
    last_pr_opened = models.DateTimeField()
    
    sync_created = models.DateTimeField(auto_now_add=True)
    sync_last_updated = models.DateTimeField(auto_now_add=True)

    # Ignores a package in the lists
    ignore = models.BooleanField(default=False)

    class Meta:
        unique_together = ('owner', 'repo')

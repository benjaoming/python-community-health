from django.db import models
from django.utils import timezone


class Project(models.Model):
    """
    This is a prototype :)
    """
    
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
    
    def __str__(self):
        return "{}/{}".format(self.owner, self.repo)


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
    
    popularity = models.FloatField()

    popularity_vs_issues = models.FloatField(null=True)
    
    popularity_vs_contributors = models.FloatField()

    # Stuff that may be none (if issues disabled, no merged pulls etc..)

    closed_issues_per_day = models.FloatField(null=True)

    popularity_vs_closed_issues_per_day = models.FloatField(null=True)

    days_since_last_pr_merge = models.FloatField(null=True)

    popularity_vs_days_since_last_pr_merge = models.FloatField(null=True)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def update(self):
        """
        Doesn't save anything
        """
        
        self.open_issues = self.project.open_issues
        self.closed_issues = self.project.closed_issues
        self.open_pulls = self.project.open_pulls
        self.closed_pulls = self.project.closed_pulls

        days_alive = (timezone.now() - self.project.created_at).days
        
        self.popularity = self.project.stars + self.project.watchers + self.project.forks
        
        if self.open_issues:
            self.popularity_vs_issues = self.popularity / float(self.open_issues)
        
        self.popularity_vs_contributors = self.popularity / float(self.project.contributors)

        if days_alive:
            self.closed_issues_per_day = self.closed_issues / float(days_alive)

        if self.project.last_pr_closed:
            if self.closed_issues_per_day:
                self.popularity_vs_closed_issues_per_day = self.popularity / self.closed_issues_per_day
            self.days_since_last_pr_merge = (timezone.now() - self.project.last_pr_closed).days

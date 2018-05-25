import time

from django.core.management.base import BaseCommand
from django.conf import settings
from github3 import login

from ... import models


class Command(BaseCommand):
    help = 'Updates database with Github data'

    def handle(self, *args, **options):
        self.options = options
        self.gh = login(
            settings.GITHUB_USERNAME,
            password=settings.GITHUB_PASSWORD
        )
        self.update()

    def add_arguments(self, parser):
        parser.add_argument(
            '--repo',
            type=str,
            dest='repo',
            help="Only update --repo=<owner/repo>",
        )

    def search_issues(self, owner, repo, issue_type="issue", state="open",
            sort="created", order="desc"):
        """
        :returns: (count, latest_created, latest_updated)
        """
        issues = self.gh.search_issues(
            "repo:{owner}/{repo} type:{type} state:{state}".format(
                owner=owner,
                repo=repo,
                type=issue_type,
                state="open"
            ),
            sort=sort,
            order=order,
        )

        # Get the first item in result, this also populates total_count
        try:
            issue = issues.next()
            return (
                issues.total_count,
                issue.issue.created_at,
                issue.issue.updated_at
            )
        except StopIteration:
            return 0, None, None
        

    def update(self):
        
        # Fetches top 100 python projects
        results_total = 100
        
        if self.options['repo']:
            owner, repo = self.options['repo'].split("/")
            results_total = 0  # not used
            results = self.gh.search_repositories(
                query="user:{} repo:{}".format(owner, repo)
            )
        else:
            results = self.gh.search_repositories(query='language:python', sort='stars', number=results_total)
        
        for cnt, r in enumerate(results):
            
            # Create or update existing data
            try:
                p = models.Project.objects.get(
                    owner=r.repository.owner,
                    repo=r.repository.name,
                )
            except models.Project.DoesNotExist:
                p = models.Project(
                    owner=r.repository.owner,
                    repo=r.repository.name,
                )
            
            # Fetch expanded Repository instance, since the iterator only has
            # ShortRepository
            repo = self.gh.repository(r.repository.owner, r.repository.name)
            print("Now scraping {repo} ({cnt}/{total})".format(
                repo=repo,
                cnt=cnt + 1,
                total=results_total or results.total_count,
            ))
            
            # More information is in this dict than the attributes populated...
            repo_dict = repo.as_dict()
            
            p.stars = repo_dict['stargazers_count']
            p.watchers = repo_dict['subscribers_count']
            p.forks = repo_dict['forks_count']
            
            # This is ugly, but cannot find the count anywhere else :/
            p.contributors = len(list(repo.contributors()))

            p.open_pulls, p.last_pr_opened, __ = self.search_issues(
                repo.owner, repo.name, issue_type="pr", state="open")
            
            p.closed_issues, __, p.last_issue_closed = self.search_issues(
                repo.owner, repo.name, issue_type="issue", state="closed", sort="updated")

            p.closed_pulls, p.last_pr_closed, __ = self.search_issues(
                repo.owner, repo.name, issue_type="pr", state="closed", sort="updated")

            p.open_issues = repo_dict['open_issues_count']
            p.created_at = repo_dict['created_at']
            p.updated_at = repo_dict['updated_at']
            p.save()

            # Then sleep a little bit because of Github
            time.sleep(0.5)

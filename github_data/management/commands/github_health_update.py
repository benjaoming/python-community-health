from django.core.management.base import BaseCommand
from django.conf import settings
from github3 import login

from ...models import GithubProject


class Command(BaseCommand):
    help = 'Updates database with Github data'

    def handle(self, *args, **options):
        self.stdout.write("Please enter the Github password:")
        self.password = input()
        self.username = options['username']
        self.update()

    def add_arguments(self, parser):
        parser.add_argument('username', type=str)

    def update(self):
        gh = login(settings.GITHUB_USERNAME, password=settings.GITHUB_PASSWORD)
        results = gh.search_repositories(query='language:python', sort='stars', number=1)
        print(dir(results))
        
        for r in results:
            print(dir(r.repository))

            try:
                p = GithubProject.objects.get(
                    owner=r.repository.owner,
                    repo=r.repository.name,
                )
            except GithubProject.DoesNotExist:
                p = GithubProject(
                    owner=r.repository.owner,
                    repo=r.repository.name,
                )
            
            p.stars = r.repository.stargazers
            p.watchers = r.repository.subscribers
            p.contributors = r.repository.contributors
            
            print(p.owner, p.repo)
            open_prs = gh.search_issues(
                query="type:pr repo:{}/{}".format(p.owner, p.repo)
            )
            print(open_prs.total_count)
            p.open_pr_count = r.repository.pull_requests
            p.save()

from django.core.management.base import BaseCommand

from ... import models


class Command(BaseCommand):
    help = 'Updates scoring based on current data'

    def handle(self, *args, **options):
        self.options = options
        self.update()

    def add_arguments(self, parser):
        parser.add_argument(
            '--rewind',
            action='store_true',
            dest='rewind',
            help="Replace the latest stats",
        )

    def update(self):
        if self.options['rewind']:
            models.Scoring.objects.all().delete()
        for project in models.Project.objects.filter(ignore=False):
            s = models.Scoring(project=project)
            s.update()
            s.save()

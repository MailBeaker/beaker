
from django.core.management.base import BaseCommand

from base import get_celery_app

from beaker.models import Domain


class Command(BaseCommand):
    help = 'Adds all domains from the database to the message queue'

    def handle(self, *args, **options):

        app = get_celery_app()

        domains = Domain.objects.all()
        for domain in domains:
            try:
                app.send_task(
                    'get_user_list_v1',
                    args=[domain.domain_name]
                )
            except Exception, e:
                self.stdout.write("Error adding %s to the task queue" % domain.domain_name)
                self.stdout.write(e)

        self.stdout.write("Successfully added all domains to the queue")

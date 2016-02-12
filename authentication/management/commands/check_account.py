
from django.core.management.base import BaseCommand

from base import get_celery_app

from authentication.models import EmailMeta


class Command(BaseCommand):
    help = 'Adds all emails from the database to the message queue'

    def handle(self, *args, **options):

        app = get_celery_app()

        users = EmailMeta.objects.all()
        for user in users:
            try:
                app.send_task(
                    'check_account_v1',
                    args=[user.email, user.id, user.history_id]
                )
            except Exception, e:
                self.stdout.write("Error adding %s to the task queue" % user.email)
                self.stdout.write(e)

        self.stdout.write("Successfully added all users to the queue")

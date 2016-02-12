
from django.core.management.base import BaseCommand

from authentication.models import MBUser
# from authentication.models import EmailMeta
from authentication.models import UserMeta

# from base import get_celery_app

from beaker.models import Domain
from beaker.models import Organization
from beaker.models import Rule
# from beaker.models import Message
# from beaker.models import RuleMatch
# from beaker.models import Link


# We currently only support one organization in this script for now.
# Everything gets added to this org.
organization = {
    'name': 'MailBeaker',
    'address_1': '123 Any Street',
    'address_2': 'Suite 1001',
    'city': 'New York',
    'state': 'NY',
    'phone': '5555555555',
    'zip': '10108'
}

# Only one domain for now
domain = {
    'domain_name': 'mailbeaker.com',
    'whitelisted': True,
    'blacklisted': False,
}

users = [
    {
        'email': 'someone@example.com',
        'first_name': '',
        'last_name': '',
        'is_active': True,
        'is_admin': True,
        'is_platform': False,
        'is_webapp': False,
    }
]

#   actions
#       0 = Pass
#       1 = Warn
#       2 = Block
#
#   mods
#       0 = Ignore this field for this rule
#       1 = Equals the value
#       2 = Does not equal the value
#       3 = Contains the value
#       4 = Does not contain the value
#       5 = Starts with the value
#       6 = Ends with the value

rules = [
    {
        'description': 'Block russian domains',
        'alert_admins': True,
        'action': 2,
        'sender_mod': 6,
        'sender_value': '.ru',
        'receiver_mod': 0,
        'subject_mod': 0,
        'url_mod': 0,
        'body_mod': 0,
    },
    {
        'description': 'Warn viagra subject',
        'alert_admins': True,
        'action': 1,
        'sender_mod': 0,
        'receiver_mod': 0,
        'subject_mod': 3,
        'subject_value': 'viagra',
        'url_mod': 0,
        'body_mod': 0,
    },
    {
        'description': "Anaconda don't want none",
        'alert_admins': True,
        'action': 2,
        'sender_mod': 0,
        'receiver_mod': 3,
        'receiver_value': 'anaconda',
        'subject_mod': 0,
        'url_mod': 0,
        'body_mod': 0,
    }
]


class Command(BaseCommand):
    help = 'Creates a database with test data for local testing.'

    def handle(self, *args, **options):

        # Create the organization
        org = Organization(**organization).save()
        if not org:
            self.stdout.write("Org failed")
            return

        self.stdout.write("Successfully created the MailBeaker organization")

        # Create the domain in the organization
        dom = Domain(organization=org, **domain)
        self.stdout.write("Successfully created the MailBeaker domain")

        # Create all of the users in the domain
        for user in users:
            mb_user = MBUser(**user).save()
            user_meta = UserMeta(user=mb_user, organization=org)
            self.stdout.write("Successfully created the %s user and associated meta" % mb_user.email)

        # Create all of the rules
        for rule in rules:
            rule_entity = Rule(domain=dom, **rule)
            self.stdout.write("Successfully created the rule: %s" % rule['description'])

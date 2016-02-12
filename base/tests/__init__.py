

from rest_framework.test import APITestCase


from authentication.models import MBUser
from authentication.models import UserMeta

from beaker.models import Organization
from beaker.models import Domain


class BaseTestCase(APITestCase):

    def setUp(self):
        """
        Sets up a number of test entites in the database for testing.

        Included:
            user: A webapp user
            organization: An organization that user belongs to
            domain: A domain that belongs to organization
        """

        # Creating Users
        self.user = MBUser(
            email='test@test.com',
            first_name='test',
            last_name='tester',
            is_admin=False,
            is_platform=False,
            is_webapp=True,
        )

        self.user.set_password('test')
        self.user.save()

        self.client.login(username='test@test.com', password='test')

        # Organization
        self.organization = Organization(
            name='Test Organization',
            address_1='123 Any Street',
            address_2='Suite 001',
            city='New York',
            state='NY',
            phone='555-555-1234'
        )
        self.organization.save()

        self.user_meta = UserMeta(
            user=self.user,
            organization=self.organization
        )
        self.user_meta.save()

        # Domain
        self.domain = Domain(
            domain_name='test.com',
            organization=self.organization,
            whitelisted=False
        )
        self.domain.save()

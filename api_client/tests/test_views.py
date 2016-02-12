
from rest_framework import status
from rest_framework.reverse import reverse

from authentication.models import MBUser
from authentication.models import UserMeta

from base.tests import BaseTestCase

from beaker.models import Organization


class RootTestCase(BaseTestCase):

    def test_get_root(self):
        """
        Ensure we can get the root client API.
        """
        url = reverse('client-api-root')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserTestCase(BaseTestCase):

    def test_get_user_detail(self):
        """
        Ensure we can get the user detail view for the current user.
        """
        url = reverse('client-user-detail', kwargs={'pk': self.user.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cant_get_user_while_logged_out(self):
        """
        Ensure that we can't get a user while not logged in.
        """
        self.client.logout()
        url = reverse('client-user-detail', kwargs={'pk': self.user.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_cant_get_other_user_detail(self):
        """
        Ensure that we can't get the user detail view for a user
        that is not currently logged in.
        """
        other_user = MBUser(
            email='other@test.com',
            first_name='other',
            last_name='otherer',
            is_admin=False,
            is_platform=False,
            is_webapp=True,
        )

        other_user.set_password('other')
        other_user.save()

        url = reverse('client-user-detail', kwargs={'pk': other_user.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # def test_update_user(self):
    #     data = {
    #         'email': 'another@test.com',
    #     }

    #     url = reverse('client-user-detail', kwargs={'pk': self.user.id})
    #     response = self.client.post(url, data)
        # self.assertEquals(response.status_code, status.HTTP_200_OK)


class OrganizationTestCase(BaseTestCase):

    def test_list_organizations(self):
        """
        Ensure that we can list the organizations we have access to and
        only organizations that we have access to.
        """
        url = reverse('client-organization-list')

        response = self.client.get(url, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data['count'], 1)
        self.assertEquals(response.data['results'][0]['id'], self.organization.id)

        other_org = Organization(
            name='Other Organization',
            address_1='123 Any Street',
            address_2='Suite 001',
            city='Ames',
            state='IA',
            phone='515-555-1234'
        )
        other_org.save()

        response = self.client.get(url, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data['count'], 1)
        self.assertEquals(response.data['results'][0]['id'], self.organization.id)

    def test_get_organization(self):
        """
        Ensure we can get the user's organization
        """
        url = reverse('client-organization-detail', kwargs={'pk': self.organization.id})
        response = self.client.get(url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data['id'], self.organization.id)

    def test_cant_get_organization_while_logged_out(self):
        """
        Ensure that we have to be logged in to access an organization.
        """
        url = reverse('client-organization-detail', kwargs={'pk': self.organization.id})
        response = self.client.get(url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data['id'], self.organization.id)

        self.client.logout()

        response = self.client.get(url)
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_cant_get_other_organization(self):
        """
        Ensure we can get organization detail view for an organization
        that the logged in user doesn't have access to.
        """
        other_org = Organization(
            name='Other Organization',
            address_1='123 Any Street',
            address_2='Suite 001',
            city='Ames',
            state='IA',
            phone='515-555-1234'
        )
        other_org.save()

        url = reverse('client-organization-detail', kwargs={'pk': other_org.id})
        response = self.client.patch(url)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_organization(self):
        """
        Ensure that we can update an organization that we have access to.
        """
        url = reverse('client-organization-detail', kwargs={'pk': self.organization.id})
        data = {
            'name': 'Updated Name'
        }
        response = self.client.patch(url, data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)


class DomainTestCase(BaseTestCase):

    def test_get_domain(self):
        """
        Ensure we can get the user's domain
        """
        url = reverse('client-domain-detail', kwargs={'pk': self.domain.id})
        response = self.client.get(url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

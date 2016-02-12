
from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied

from authentication.models import UserMeta

from beaker.models import Organization

from base.models import RandomIDModel


class WebappPermission(permissions.BasePermission):
    """
    User is a MailBeaker webapp User.  These are external users
    and should only be allowed access to their own data.
    """

    def has_permission(self, request, view):
        if request.user.is_anonymous():
            return False

        if request.user.is_admin:
            return True

        return request.user.is_webapp


class WebappMixin(object):
    permission_classes = (WebappPermission,)


class SafeMethodsMixin(object):

    safe_get_model = None

    def org_safe_get(self, user, pk):
        """
        Gets the entity for the given primary key while making
        sure that the user has access to the entity.

        This first checks if the requested entity has an organization attribute.
        If it does, it checks against that.  If there is no organization, the
        entity is checked for a domain to find the organization.

        :param user: MBUser entity
        :param pk: Primary Key to look up.
        :return: An entity
        """

        if not pk:
            raise PermissionDenied()

        if not user:
            raise PermissionDenied()

        # TODO: We need to handle multiple UserMetas in the future.
        user_meta = UserMeta.get_by_user(user)
        if not user_meta:
            raise PermissionDenied()

        try:
            entity = self.safe_get_model.get_by_id(pk)
        except AttributeError:
            raise PermissionDenied("safe_get_model must have a get_by_id method")

        if not entity:
            raise PermissionDenied("No entity found for id: %s")

        # First check for an organization on the entity itself
        if hasattr(entity, 'organization'):
            if entity.organization == user_meta.organization:
                return entity

            raise PermissionDenied()

        # Second, check for the organization based on the domain
        if hasattr(entity, 'domain'):
            if entity.domain.organization == user_meta.organization:
                return entity

            raise PermissionDenied()

        # Third, check if the object is an organization
        if isinstance(entity, Organization):
            if entity == user_meta.organization:
                return entity

        raise PermissionDenied()

from rest_framework import permissions


class SuperadminPermission(permissions.BasePermission):
    """
    User is a MailBeaker internal admin User.  These are our MailBeaker employees.
    """

    def has_permission(self, request, view):
        return request.user.is_admin


class SuperadminMixin(object):
    permission_classes = (SuperadminPermission,)


class PlatformPermission(permissions.BasePermission):
    """
    User is a MailBeaker internal platform User.  These are other servers
    controlled by MailBeaker.  Platform users have access to pretty much
    everything except for managing users.
    """

    def has_permission(self, request, view):
        if hasattr(request.user, 'is_admin') and request.user.is_admin:
            return True

        return hasattr(request.user, 'is_platform') and request.user.is_platform


class ServiceMixin(object):
    permission_classes = (PlatformPermission,)

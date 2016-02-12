
from authentication.models import UserMeta


def create_user_meta(backend, user, response, *args, **kwargs):
    UserMeta.get_or_create_user_meta(user)


from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


class HookSet(object):

    def get_blog(self, **kwargs):
        username = kwargs.get('username', None)
        return get_user_model().objects.get(username=username).blog




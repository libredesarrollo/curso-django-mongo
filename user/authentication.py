
from django.contrib.auth.models import User

class AuthByEmailBackend:

    def authenticate(self, request, username=None, password=None):

        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user

        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            user = User.objects.get(id=user_id)
            return user
        except User.DoesNotExist:
            return None
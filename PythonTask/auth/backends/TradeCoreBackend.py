from django.contrib.auth.backends import BaseBackend

class TradeCoreBackend(BaseBackend):

    def authenticate(self, request, username=None, password=None):
        # Check the username/password and return a user.
        pass

    def authenticate(self, request, token=None):
        # Check the token and return a user.
        pass

    def get_user(self, user_id):
        return None

    
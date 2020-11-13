# package: SocialNetwork.auth.backends
from typing import Tuple, Optional

import jwt
from django.conf import settings
from rest_framework import authentication, exceptions
from rest_framework.request import Request

from SocialNetwork.models import User


class JWTAuthenticationBackend(authentication.BaseAuthentication):
    """
    Authentication backend that used to authenticate the user base on the JWT token.
    """
    authentication_header_prefix = 'Token'  # The token prefix.

    def authenticate(self, request: Request) -> Optional[Tuple[User, str]]:
        """
        authenticate user request (called for every request)
        :param request: The authentication request.
        :return: The user and it's token if the user authenticated otherwise None
        """

        request.user = None  # Reset the user.

        # Get the authentication header name and the JWT that will be used for authentication.
        authentication_header = authentication.get_authorization_header(request).split()
        authentication_header_prefix = self.authentication_header_prefix.lower()

        if not authentication_header:
            return None # No header.

        if len(authentication_header) == 1:
            return None  # Invalid header, no credentials provided.

        if len(authentication_header) > 2:
            return None  # Invalid header, the Token string should not contain spaces.

        # Decoding the authentication prefix and token from the authentication header.
        authentication_prefix = authentication_header[0].decode('utf-8')
        authentication_token = authentication_header[1].decode('utf-8')

        if authentication_prefix.lower() != authentication_header_prefix:
            return None  # Mismatch between the authentication prefix

        return self.__authenticate_user_credentials(authentication_token)  # Authenticate the user.

    def __authenticate_user_credentials(self, token: str) -> Tuple[User, str]:
        """
        Authenticate the user based on the JWT token.
        :param token: The request JWT token.
        :return:
        """
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256']) # Decode the token.
        except:
            msg = 'Invalid authentication. Could not decode token.'
            raise exceptions.AuthenticationFailed(msg) # Failure decoding the token.

        try:
            user = User.objects.get(pk=payload['id']) # Find user based on his ID.
        except User.DoesNotExist:
            msg = 'No user matching this token was found.'
            raise exceptions.AuthenticationFailed(msg) # User not found.

        if not user.is_active:
            msg = 'This user has been deactivated.'
            raise exceptions.AuthenticationFailed(msg) # User not active.

        return (user, token) # Return the user with the token.

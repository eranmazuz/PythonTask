# Package: SocialNetwork.serializers

from django.contrib.auth import authenticate
from rest_framework import serializers

from SocialNetwork.models import User


class LoginSerializer(serializers.Serializer):
    """
    Used to serialize and deserialize login requests.
    """

    # Login fields
    email = serializers.CharField(max_length=254)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data) -> dict[str, str]:
        """
        Validate that the data of the serializer and authenticate the user.
        :param data: The serializer data.
        :return: The user information after authentication.
        """

        # Get the login data/
        email = data.get('email', None)
        password = data.get('password', None)

        user = authenticate(username=email, password=password)

        self.__authenticate_user(user)

        # Return user information.
        return {
            'email': user.email,
            'username': user.username,
            'token': user.token
        }

    def validate_email(self, email: str) -> str:
        """
        Run validation for the email field when running the validations,
        :param email: the email field value.
        :return: the email field value.
        """

        if email is None:
            raise serializers.ValidationError('An email address is required to log in.')

        return email

    def validate_password(self, password):
        """
        Run validation for the password field when running the validations,
        :param password: the password field value.
        :return: the password field value.
        """
        if password is None:
            raise serializers.ValidationError('A password is required to log in.')

        return password


    def __authenticate_user(self, user: User):
        """
        Authenticate the user.
        :param user: The instance of the user that want to log in.
        """

        if user is None:
            raise serializers.ValidationError('A user with this email and password was not found.')

        if not user.is_active:
            raise serializers.ValidationError('This user has been deactivated.')

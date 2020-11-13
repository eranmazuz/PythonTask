# Package: SocialNetwork.serializers

from pyhunter import PyHunter
from rest_framework import serializers

from PythonTask import settings
from ..models import User

class RegistrationSerializer(serializers.ModelSerializer):
    """
    Used to serialize and deserialize registration requests for new users.
    """

    # Ensure That the password length is minimum 8 characters.
    # The field is read only so the password will not be serialized.
    password = serializers.CharField(max_length=128, min_length=8, write_only=True)

    # Prevent the client to send token with the registration.
    token = serializers.CharField(max_length=255, read_only=True)

    def create(self, validated_data):
        """
        Creating new user from the validated data.
        :param validated_data: The data from the deserialization after verification.
        :return: The new user.
        """
        return User.objects.create_user(**validated_data)

    def validate_email(self, email):
        """
        Validate the email field.
        :param email: The email.
        :return: The email after validation
        """

        if email is None:
            raise serializers.ValidationError('Users must have an email address.')

        # Verify email using hunter.io
        hunter = PyHunter(settings.HUNTER_API_KEY)
        result = hunter.email_verifier(email)
        if result['status'] == 'invalid':
            raise serializers.ValidationError('Users must have an valid email address.')

        return email

    def validate_password(self, password):
        """
        Validate the password field.
        :param password: The password.
        :return: The validated password.
        """

        if password is None:
            raise serializers.ValidationError('Users must have a password.')

        return password

    def validate_username(self, username):
        """
        Validate the username field.
        :param username: The username.
        :return: The validate username.
        """
        if username is None:
            raise serializers.ValidationError('Users must have a username.')

        return username

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'token']





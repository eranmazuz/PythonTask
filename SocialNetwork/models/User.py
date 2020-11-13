# Package: SocialNetwork.models
from datetime import datetime, timedelta, timezone

import clearbit
import jwt
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

clearbit.key = settings.CLEARBIT_API_KEY


class UserManager(BaseUserManager):
    """
    Manager class for our own custom user.
    """

    def create_user(self, username, email, password):
        """
            Create user based on the given information.
            :param username: The user username.
            :param email: The user email.
            :param password: The user password.
            :return: A 'User' instance with the given information.
        """

        # Create User
        user = self.model(username=username, email=self.normalize_email(email))

        self.__intilize_user(user, email, password)

        return user

    def __intilize_user(self, user, email, password):
        """
           Retrieve the information from Clearbit Enrichment and initialize the user with the information and the given data.
           :param user: The user instance.
           :param email: the user email (used to get the information from Clearbit Enrichment).
           :param password: The user password.
        """
        person = clearbit.Person.find(email=email, stream=True)

        if person is None:
            user.set_password(password)
            user.save()
            return

        user.first_name = person['name']['givenName']
        user.last_name = person['name']['familyName']
        user.bio = person['bio'] or ''
        user.location_city = person['geo']['city'] or ''
        user.location_state_code = person['geo']['stateCode'] or ''
        user.location_country_code = person['geo']['countryCode'] or ''
        user.linkedin = person['linkedin']['handle'] or ''
        user.facebook = person['facebook']['handle'] or ''
        user.github = person['github']['handle'] or ''

        user.set_password(password)
        user.save()

    def create_superuser(self, username, email, password):
        """
        Create user based on the given information (super user is the same as regular user).
        :param username: The user username.
        :param email: The user email.
        :param password: The user password.
        :return: A 'User' instance with the given information.
        """
        return self.create_user(username, email, password)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom implementation for a user.
    """

    # User username.
    username = models.CharField(db_index=True, max_length=255, unique=True, blank=False, null=False,
                                validators=[UnicodeUsernameValidator()])

    # User mail
    email = models.EmailField(db_index=True, unique=True)

    # User active (to suspend user, we can set it as False)
    is_active = models.BooleanField(default=True)

    # The user is not a stuff of the admin site so he can't access it.
    is_staff = False

    # Timestamps for when the user registered and last logged in.
    joined_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    # User information that retrieved from the clearbit.
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    bio = models.CharField(max_length=400, blank=True)
    location_city = models.CharField(max_length=100, blank=True)
    location_state_code = models.CharField(max_length=50, blank=True)  # Store only state code.
    location_country_code = models.CharField(max_length=50, blank=True)  # Store only country code.
    linkedin = models.CharField(max_length=100, null=True, blank=True)
    facebook = models.TextField(max_length=100, null=True, blank=True)
    github = models.TextField(max_length=100, null=True, blank=True)

    # Points to the field that used as username when user log in.
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    # Custom manager for the 'User' model.
    objects = UserManager()

    @property
    def location(self):
        """
        Get the full user location.
        :return: the user location.
        """
        geo = [self.location_city, self.location_state_code, self.location_country_code]
        return ', '.join(filter(None, geo))

    def __str__(self):
        """
        Return string representation of the User
        :return: Representation of the user.
        """

        return self.email

    def get_full_name(self):
        """
        Return the user full name.
        :return: The user full name.
        """

        return '%s %s' % (self.first_name, self.last_name)

    def get_short_name(self):
        """
        Return the user first name.
        :return: The user first name.
        """
        return self.first_name

    def _generate_jwt_token(self) -> str:
        """
        Generate JSON Web Token (JWT) that contains the user's ID and will expire in 60 Days from the creation.
        :return: String representing the JSON Web Token containing the user ID.
        """
        """
        Generates a JSON Web Token that stores this user's ID and has an expiry
        date set to 60 days into the future.
        """

        expire_date = datetime.now() + timedelta(days=60)
        token = jwt.encode({
            'id': self.pk,
            'exp': expire_date.replace(tzinfo=timezone.utc).timestamp()
        }, settings.SECRET_KEY, algorithm='HS256')

        if isinstance(token, str):
            return token

        return token.decode('utf-8')

    @property
    def token(self):
        """
        Return the user's token
        :return: The user's token.
        """
        return self._generate_jwt_token()

    def create_post(self, title, body):
        self.posts.create(title=title, body=body)

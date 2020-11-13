# Package: Bot.Helper
import random
import string

random.seed() # Create seed based on the system time.
def get_rule(name: str, default: any) -> any:
    """
    Retrieve the field value from the configuration file.
    :param name: the name of the field in the configuration file
    :param default: value to return when there is failure retrieving the field value from the configuration file
    :return: The field value or default value.
    """

    # Load the configuration file and return the field value (or the given value if the field not found).
    try:
        from Bot import Settings
        return getattr(Settings, name, default)

    # When error raised, return the given value.
    except:
        return default


class Generator:
    """
    Generator class to generate data.
    """

    @staticmethod
    def generate_user() -> dict[str, str]:
        """
        Generate random user data.

        :return: The user information
        """
        user = {
            'username': Generator.generate_user_name(),
            'password': Generator.generate_password(),
            'email': Generator.generate_mail()
        }

        return user

    @staticmethod
    def generate_user_name() -> str:
        """
        Generate random username.
        :return: The username
        """

        username = "".join(random.choice(string.ascii_lowercase) for _ in range(2))
        username = username + "".join(random.choice(string.digits) for _ in range(4))
        username = username + "".join(random.choice(string.ascii_uppercase) for _ in range(5))
        return username

    @staticmethod
    def generate_password() -> str:
        """
        Generate random password.
        :return: The password.
        """

        password = "".join(random.choice(string.ascii_lowercase) for _ in range(2))
        password = password + "".join(random.choice(string.digits) for _ in range(4))
        password = password + "".join(random.choice(string.ascii_uppercase) for _ in range(5))
        return password

    @staticmethod
    def generate_mail() -> str:
        """
        Generate random mail.
        :return: The mail.

        """
        # Because Clearbit enrichment is used to supply the additional data on user sign up
        # There is need to use real mails to get the user data.

        mails = ['alex@clearbit.com', 'harlow@clearbit.com', 'eoghan@intercom.io', 'brian@airbnb.com',
                 'arash@dropbox.com', 'peter@segment.com', 'dom@tray.io', 'john@stripe.com', 'josh@domo.com',
                 'crobbins@cisco.com']
        return random.choice(mails)

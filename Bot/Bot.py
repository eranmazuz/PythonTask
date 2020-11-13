# package: Bot.Bot

import logging
import random
import string

import requests

from Bot.Helper import get_rule, Generator

# Set format to the bot logs.
logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')


def sort_by_post_count(user):
    """
    Function that used in sort to sort the users by the number of posts they created.
    :param user: The user to sort.
    :return: The number of posts the user created.
    """

    return user['num_of_posts']


def filter_no_liked_posts(post):
    """
    Function that used in filter to filter the posts that have no likes.
    :param post: The post to filter
    :return: If the post don't have likes.
    """
    return post['likes_count'] == 0


def map_to_users(post):
    """
    Function that used in map to get the creators of the posts
    :param post: The post to map.
    :return: The username of the post creator.
    """
    return post['creator']


def filter_user_liked_posts(post):
    """
    Function that used in filter to filter the posts that the user already liked.
    :param post: The post to filter.
    :return: If the user already liked the post.
    """
    return not post['is_user_like']


class Bot:
    """
    Bot to demonstrate How the Django API is used.
    """
    NUMBER_OF_USERS = 3  # Maximum number of new users to create.
    MAX_POSTS_PER_USER = 5  # Maximum number of posts the user can create.
    MAX_LIKES_PER_USER = 3  # Maximum number of likes the user can do.

    def __init__(self) -> None:
        """
        Constructor to initialize the bot.
        """
        # Load the bot default configuration into the bot.
        self.__load_default_configuration()

    def __load_default_configuration(self) -> None:
        """
        Method to load the default configuration bot.
        """
        self.number_of_users = get_rule('NUMBER_OF_USERS', Bot.NUMBER_OF_USERS)
        self.max_posts_per_user = get_rule('MAX_POSTS_PER_USER', Bot.NUMBER_OF_USERS)
        self.max_likes_per_user = get_rule('MAX_LIKES_PER_USER', Bot.MAX_LIKES_PER_USER)

    def start_activity(self):
        """
        Method to start the bot activity.
        :return:
        """
        self.users = []
        self.__load_configuration()  # Load configurations for the bot run.
        self.__signup_users()  # Sign Up uses
        self.__create_users_posts()  # Create posts for the users.
        self.__like_user_posts() # Like the posts.

    def __like_user_posts(self):
        """
        Method to for the users to like posts according to the task rules.
        :return:
        """
        self.users.sort(key=sort_by_post_count, reverse=True)  # Sort user by the number of posts they created.

        for user in self.users:

            for _ in range(self.max_likes_per_user):  # Run until user reach max likes.

                posts = self.__request_posts(user)   # Get all the posts.
                logging.warning('User with the email %s received %s posts.' % (user['email'], len(posts)))

                logging.warning('Filtering for posts with no likes.')
                unliked_posts = list(filter(filter_no_liked_posts, posts))  # filter the posts with no likes.
                logging.warning('There are %s posts with no likes.' % len(unliked_posts))

                # Stop the bot if all the posts are liked.
                if len(unliked_posts) == 0:
                    logging.warning('All the posts are liked, stopping the bot.')
                    return

                # Get the usernames of the creators of the unliked posts.
                creators = self.__get_creators_posts(posts, user)

                # Stop the bots if the only posts that not liked are the current user posts (see Decisions in the readme)
                if len(creators) == 0:
                    logging.warning(
                        "Only the current user posts are not liked and user can't like his own posts, stopping the bot.")
                    return

                # Select random creator of the unliked posts.
                random.seed()
                creator = random.choice(list(creators))

                creator_posts = self.__get_users_posts(user, creator) # Get the creator posts.

                # Choose random post form the creator posts that you user didn't already liked.
                creator_posts_user_not_liked = list(filter(filter_user_liked_posts, creator_posts))
                post_to_like = random.choice(creator_posts_user_not_liked)

                self.__post_to_like(user, post_to_like) # Like the post.

            logging.warning('User with the email %s reached max likes.' % user['email'])
        logging.warning('All the users reached max likes, stopping the bot.')

    def __post_to_like(self, user, post):
        """
        Like user post.
        :param user: The logged user.
        :param post: The post to like
        """
        logging.warning('Liking post with title %s by user %s.' % (post['title'], post['creator']))

        # Send post request to like the post with the logged user JWT token.
        headers = {'Authorization': 'Token %s' % (user['token'])}
        posts_address = '%s/%s%s/' % (self.site_address, self.posts_path, post['id'])

        response = requests.post(posts_address, headers=headers)
        logging.warning('Post with title %s by user %s is successfully liked.' % (post['title'], post['creator']))

    def __get_users_posts(self, user, creator_username):
        """
        Get requested user post.
        :param user: The logged user.
        :param creator_username: The username of the user that you want to get the post from.
        :return:
        """
        logging.warning('Requesting the posts for the user with the username %s.' % creator_username)

        # Send post request to get the requested user posts with the logged user JWT token.
        headers = {'Authorization': 'Token %s' % (user['token'])}
        posts_address = '%s/%s%s/%s' % (self.site_address, self.users_path, creator_username, self.posts_path)
        response = requests.get(posts_address, headers=headers)

        logging.warning('Successfully received the posts of the user %s.' % creator_username)
        return response.json()

    def __get_creators_posts(self, posts, user):
        """
        Get the creators of the posts.
        :param posts: The posts.
        :param user: The logged users.
        :return: The creators of the posts (excluding the logged user).
        """

        creators = map(map_to_users, posts)

        # Filtering the posts that not of the logged user becasue the user can't like his own posts.
        creators = filter(lambda creator: creator != user['username'], creators)

        return set(creators)

    def __request_posts(self, user):
        """
        Request all the posts.
        :param user: The logged user.
        :return: JSON of all the posts.
        """

        logging.warning('User with the email %s requesting posts.' % user['email'])

        # Send post request to get all the posts with the logged user JWT token.
        headers = {'Authorization': 'Token %s' % (user['token'])}
        posts_address = '%s/%s' % (self.site_address, self.posts_path)
        response = requests.get(posts_address, headers=headers)

        logging.warning('User with the email %s successfully received the posts.' % user['email'])

        return response.json()

    def __load_configuration(self) -> None:
        """
        Method to load the configuration for the bot run.
        """
        self.site_address = get_rule('SITE_ADDRESS', None)
        self.login_path = get_rule('LOGIN_PATH', None)
        self.signup_path = get_rule('SIGNUP_PATH', None)
        self.posts_path = get_rule('POSTS_PATH', None)
        self.users_path = get_rule('USERS_PATH', None)

        self.__verify_configuration()  # Verify the required configurations.

    def __verify_configuration(self) -> None:
        """
        Verification of the configurations for the run.
        """

        if self.site_address is None:
            raise Exception("Invalid configuration")

        if self.login_path is None:
            raise Exception("Invalid configuration")

        if self.signup_path is None:
            raise Exception("Invalid configuration")

        if self.posts_path is None:
            raise Exception("Invalid configuration")

        if self.users_path is None:
            raise Exception("Invalid configuration")

    def __signup_users(self) -> list[int]:
        """
        Create users and register them.
        :return:
        """

        for _ in range(self.number_of_users):
            data = self.__signup_user()
            self.__signin_user(data)

    def __signup_user(self) -> dict[str, str]:
        """
        Create user and register him.
        :return:
        """
        sign_up_address = '%s/%s' % (self.site_address, self.signup_path)

        logging.info('Registering users.')

        # Because mail is used as login identification, it's unique and becuase we have limited
        while True:

            data = Generator.generate_user()  # Generate user data.
            logging.warning('Registering user with mail %s.' % data['email'])
            response = requests.post(sign_up_address, data=data)  # Send registration request for the new user.

            # End the loop if the user is registred.
            if response.status_code == 201:
                logging.warning('User with mail %s been registered successfully.' % data['email'])
                return data

            logging.warning('User with the mail %s already exist, trying another mail.' % data['email'])

    def __signin_user(self, data: dict[str, str]):
        """
        Log in the user.
        :param data: The user credentials.
        """
        sign_in_address = '%s/%s' % (self.site_address, self.login_path)
        logging.warning('Login user with mail %s.' % data['email'])

        response = requests.post(sign_in_address, data=data)
        self.users.append(response.json())
        logging.warning('User with mail %s is successfully logged in.' % data['email'])

    def __create_users_posts(self):
        """
        Create posts for the users.
        """
        for user in self.users:
            # Record the number of posts the user made so the users can be sorted by them later.
            user['num_of_posts'] = random.randint(1, int(self.max_posts_per_user))
            logging.warning('Creating %s posts for the user with the email %s.' % (user['num_of_posts'], user['email']))

            # Create posts.
            for _ in range(user['num_of_posts']):
                self.create_post_user(user)

            logging.warning(
                'User with the email %s successfuly create %s posts.' % (user['email'], user['num_of_posts']))

    def create_post_user(self, user):
        """
        Create post for the user.
        :param user: The logged user.
        """
        headers = {'Authorization': 'Token %s' % (user['token'])}
        posts_address = '%s/%s' % (self.site_address, self.posts_path)

        # Create post information (randomized data).
        title = "".join(random.choice(string.ascii_letters) for _ in range(10))
        body = "".join(random.choice(string.ascii_letters) for _ in range(20))
        data = {'title': title, 'body': body}

        # Send post request to create the logged user post with the logged user JWT token.
        response = requests.post(posts_address, headers=headers, data=data)
        logging.warning('User with the email %s successfully created post with the title %s.' % (user['email'], title))

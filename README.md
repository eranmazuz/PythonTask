# Python Engineer Task @ TradeCore
Trade code project Task.

Sorry for the lack of automated testing, Because lack of time I only tested the features manually and didn't build unit test for them.

##Requirements
* Python 3.9

##Installation
It's recommended to use python virtual environment to run the project.

To install the project required packages: 

`pip install -r requirements.txt`

To initialize the site:

`python manage.py migrate`

`python manage.py runserver`

## Run the bot
After the packages been installed and the site is up, to run the bot:

`python main.py`

The bot will print logs of it's run.

## Decisions

### Bot configuration file
I chose to use python file as the Bot configuration file for the following reasons: 
* The ability to document the configuration file help in the understanding and maintaining the configurations.
* Organize and categorization of the configurations.   
* Simplify the configuration loading and lower the dependency in external packages.



### Retrying user signup
Because the bot use have limited amount of mails to choose from and the mail used and identifier for login,
if the registration failed a new user with different email is generated until the new user is successfully signed up.


### Issue with the "like" activity
According to the rules of the "like" activity:
* user performs "like" activity until he reaches max likes.
* if there is no posts with 0 likes, bot stops.
* user cannot like their own posts.

This create a bug in the case when the only posts that are not liked are the current user posts.
so I needed to stop the bot when this case.
"""
Things to have in mind:

1:
    Number of subscribed channels might have to be locked to a limit
    depending on hardware capabilities

2:
    Only count one Kappa per user to avoid counting spam and only get genuine
    count distributed through out all the users
"""

from datetime import datetime

import twitch

# from .db import db
from .pony_db import db, Chat, Channel, query_message_per_second
from pony.orm import *

"""
ENVIRONMENT VARIABLES

"""
CLIENT_ID = "lnkcgelww2qsqynefsgk487pfuk1wx"
NICKNAME = "peacewarlando"
OAUTH = "oauth:q6x6bwve0ea0wnzucnbtxsu9zu5lvy"


"""
TWITCH LOGIC

"""

# Init Twitch API
helix_api = twitch.Helix(client_id=CLIENT_ID)


def channel_exists(channel):
    """
    check if channel exists on Twitch

    :param channel: Channel ID
    :return:
    """
    return helix_api.user(channel)


@db_session
def log_message(message):
    """
    Log message in Chat DB table

    :param message: Message Object with channel, sender & text
    :return:
    """
    channel = message.channel
    sender = message.sender
    text = message.text

    chat = Chat(
        channel=Channel.get(channel_id=channel),
        sender=sender,
        message=text,
        date_time=datetime.now(),
    )

    commit()

    # query_time_second = query_message_per_second(channel)

    # print("msg per sec", query_time_second)


@db_session
def track_channel(channel):
    """
    Track channel and add it to DB if channel exists on twitch
    and it does not exist on DB

    :param channel: channel_id
    :return: Boolean
    """

    if channel_exists(channel) and not Channel.get(channel_id=channel):
        # Add channel to DB
        Channel(channel_id=channel)
        commit()

        # Subscribe to chat
        twitch.Chat(channel=f"#{channel}", nickname=NICKNAME, oauth=OAUTH).subscribe(
            log_message
        )

        return True

    print("This channel does not exist on Twitch or was already subscribed to!")

    return False

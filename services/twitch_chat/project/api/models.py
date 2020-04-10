import os
from pony.orm import *
from datetime import datetime
import twitch

db = Database()


class Channel(db.Entity):
    channel_id = Required(str, unique=True)
    chat = Set("Chat")


class Chat(db.Entity):
    channel = Required(Channel)
    date_time = Required(datetime, precision=0)
    sender = Required(str)
    message = Required(str)


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


# TODO: This code is not respecting the DRY principle
@db_session
def query_kappa_per_minute(channel):
    query_channel = Chat.select(lambda m: m.channel.channel_id == channel)

    query_date = query_channel.filter(
        lambda m: m.date_time.date() == datetime.now().date()
    )

    query_time_hour = query_date.filter(
        lambda m: m.date_time.hour == datetime.now().hour
    )

    query_time_minute = query_time_hour.filter(
        lambda m: m.date_time.minute == datetime.now().minute
    )

    query_kappa = select(
        chat.sender for chat in query_time_minute if "Kappa" in chat.message
    ).count()

    return query_kappa


@db_session
def query_message_per_minute(channel):
    query = Chat.select(lambda m: m.channel.channel_id == channel)
    query_date = query.filter(lambda m: m.date_time.date() == datetime.now().date())

    query_time_hour = query_date.filter(
        lambda m: m.date_time.hour == datetime.now().hour
    )

    query_time_minute = query_time_hour.filter(
        lambda m: m.date_time.minute == datetime.now().minute
    ).count()

    return query_time_minute


@db_session
def query_message_per_second(channel):
    query = Chat.select(lambda m: m.channel.channel_id == channel)
    query_date = query.filter(lambda m: m.date_time.date() == datetime.now().date())

    query_time_hour = query_date.filter(
        lambda m: m.date_time.hour == datetime.now().hour
    )

    query_time_minute = query_time_hour.filter(
        lambda m: m.date_time.minute == datetime.now().minute
    )

    query_time_second = query_time_minute.filter(
        lambda m: m.date_time.second == datetime.now().second
    ).count()

    return query_time_second


@db_session
async def init_subscriptions(app):
    """
    Once the server starts subscribe to all channels in DB
    """
    NICKNAME = os.environ.get("NICKNAME")
    OAUTH = os.environ.get("OAUTH")

    channels = Channel.select()[:]

    for channel in channels:
        twitch.Chat(
            channel=f"#{channel.channel_id}", nickname=NICKNAME, oauth=OAUTH
        ).subscribe(log_message)


def generate_db(db_path):
    db.bind(provider="sqlite", filename=db_path, create_db=True)
    db.generate_mapping(create_tables=True)


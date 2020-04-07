"""
Things to have in mind:

1:
    Number of subscribed channels might have to be locked to a limit
    depending on hardware capabilities

2:
    Only count one Kappa per user to avoid counting spam and only get genuine
    count distributed through out all the users
"""

import sqlite3
from datetime import datetime

import twitch

"""
ENVIRONMENT VARIABLES

"""
CLIENT_ID = 'lnkcgelww2qsqynefsgk487pfuk1wx'
NICKNAME = 'peacewarlando'
OAUTH = 'oauth:q6x6bwve0ea0wnzucnbtxsu9zu5lvy'

"""
DATABASE & MODELS

"""

# Connect DB
# Since Twitch API is using threads we need to set
# check_same_thread to False.
# Also we need to search for Kappa with case sensitive on.
conn = sqlite3.connect('strafe-twitch.db', check_same_thread=False)
c = conn.cursor()
c.execute("PRAGMA case_sensitive_like=ON;")


def create_table(cur, create_table_sql):
    """
    create a table from the create_table_sql statement

    :param cur: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        cur.execute(create_table_sql)
    except Exception as e:
        print(e)


sql_create_channel_table = " CREATE TABLE IF NOT EXISTS channel (id integer PRIMARY KEY, channel_id text UNIQUE); "

sql_create_chat_table = """ CREATE TABLE IF NOT EXISTS chat (
                               id integer PRIMARY KEY,
                               channel text NOT NULL,
                               date_time text NOT NULL,
                               sender text NOT NULL,
                               message text NOT NULL,
                               FOREIGN KEY (channel) REFERENCES channel (channel_id)
                           ); """

create_table(c, sql_create_channel_table)
create_table(c, sql_create_chat_table)

"""
TWITCH LOGIC

"""

# Init Twitch API
helix_api = twitch.Helix(client_id=CLIENT_ID)


def kappa_per_minute(channel):
    """
    Get Kappa per minute count.

    :param channel: Twitch Channel Id
    :return: Counter
    """
    now = datetime.now().strftime("%b %d %Y %H:%M")
    c.execute(
        f"""
            SELECT COUNT(DISTINCT sender)
            FROM
                chat
            WHERE
                message LIKE "%Kappa%"
                AND
                date_time LIKE ?
                AND 
                channel = ?;
        """,
        (f"%{now}%", channel)
    )

    return c.fetchone()[0]


def get_msg_count_per_sec(channel):
    """
    Get messages per second count

    :param channel: Twitch Channel Id
    :return: Counter
    """
    now = datetime.now().strftime("%b %d %Y %H:%M:%S")
    c.execute(
        f"""
            SELECT COUNT(*)
            FROM
                chat
            WHERE
                date_time = ? AND channel = ?;
        """,
        (now, channel)
    )

    return c.fetchone()[0]


def get_msg_count_per_min(channel):
    """
    Get messages per minute count

    :param channel: Twitch Channel Id
    :return: Counter
    """
    now = datetime.now().strftime("%b %d %Y %H:%M")
    c.execute(
        f"""
            SELECT COUNT(*)
            FROM
                chat
            WHERE
                date_time LIKE ? AND channel = ?;
        """,
        (f"%{now}%", channel)
    )

    return c.fetchone()[0]


def channel_exists(channel):
    """
    check if channel exists on Twitch

    :param channel: Channel ID
    :return:
    """
    return helix_api.user(channel)


def channel_in_db(channel):
    """
    check if channel exists on DB

    :param channel: channel_id
    :return: channel_id OR False
    """
    c.execute(f"SELECT channel_id FROM channel WHERE channel_id = '{channel}'")
    r = c.fetchone()
    return r[0] if r else False


def log_message(message):
    global conn

    channel = message.channel
    sender = message.sender
    text = message.text

    now = datetime.now().strftime("%b %d %Y %H:%M:%S")

    c.execute(
        f"""
            INSERT INTO chat (channel, sender, message, date_time)
            VALUES (?, ?, ?, ?)
        """,
        (channel, sender, text, now)
    )

    conn.commit()


def track_channel(channel):
    """
    Track channel and add it to DB if channel exists on twitch
    and it does not exist on DB

    :param channel: channel_id
    :return:
    """
    if channel_exists(channel) and not channel_in_db(channel):
        c.execute(f"INSERT INTO channel (channel_id) VALUES ('{channel}')")
        conn.commit()
        twitch.Chat(channel=f'#{channel}', nickname=NICKNAME, oauth=OAUTH).subscribe(log_message)
    else:
        print("This channel does not exist or was already subscribed to!")
        # twitch.Chat(channel=f'#{channel}', nickname=NICKNAME, oauth=OAUTH).subscribe(log_message)


# track_channel("esl_csgo")

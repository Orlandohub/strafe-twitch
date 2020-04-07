"""
Things to have in mind:

1:
Number of subscribed channels might have to be locked to a limit
depending on hardware capabilities

2:
The reasoning behind immediately querying the chat table for message counts
after each insert is so we can store the updated result on a object which
then can be accessed by a subscriber every second instead of querying the DB
every second from the subscriber. that second approach would not be so precise
since during an entire second multiple entries might happen and would not be
retrieved.
Eventually the ideal solution would be to subscribe directly to the DB which
according to my research it's not possible with SQLite.
"""

import time
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
conn = sqlite3.connect('strafe-twitch.db', check_same_thread=False)
c = conn.cursor()


def create_table(cur, create_table_sql):
    """ create a table from the create_table_sql statement
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

msg_counter = {
    "msg_per_sec": 0,
    "msg_per_min": 0
}


def get_msg_count_per_sec(channel):
    """ Get messages per second count
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
    """ Get messages per minute count
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


def log_message(message):
    global msg_counter
    global conn

    channel = message.channel
    sender = message.sender
    text = message.text

    now = datetime.now().strftime("%b %d %Y %H:%M:%S")
    # now_sec = datetime.now().second

    c.execute(
        f"""
            INSERT INTO chat (channel, sender, message, date_time)
            VALUES (?, ?, ?, ?)
        """,
        (channel, sender, text, now)
    )

    conn.commit()

    msg_counter['msg_per_sec'] = get_msg_count_per_sec(channel)
    msg_counter['msg_per_min'] = get_msg_count_per_min(channel)




def channel_exists(channel):
    """ check if channel exists on Twitch
    :param channel: Channel ID
    :return:
    """
    return helix_api.user(channel)


def channel_in_db(channel):
    """ check if channel exists on DB
    :param channel: channel_id
    :return: channel_id OR False
    """
    c.execute(f"SELECT channel_id FROM channel WHERE channel_id = '{channel}'")
    r = c.fetchone()
    return r[0] if r else False


def track_channel(channel):
    """ Track channel and add it to DB if channel exists on twitch
    and it does not exist on DB

    :param channel: channel_id
    :return:
    """
    if channel_exists(channel) and not channel_in_db(channel):
        c.execute(f"INSERT INTO channel (channel_id) VALUES ('{channel}')")
        conn.commit()
        twitch.Chat(channel=f'#{channel}', nickname=NICKNAME, oauth=OAUTH).subscribe(log_message)
        while True:
            print("PER MIN", msg_counter['msg_per_min'])
            print("PER SEC", msg_counter['msg_per_sec'])
            time.sleep(1)
    else:
        print("This channel does not exist or was already subscribed to!")


track_channel("mrfreshasian")

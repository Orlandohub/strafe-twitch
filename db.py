"""
DATABASE & MODELS

"""

import sqlite3
from datetime import datetime




# Connect DB
# Since Twitch API is using threads we need to set
# check_same_thread to False.
# Also we need to search for Kappa with case sensitive on.
sql_create_channel_table = " CREATE TABLE IF NOT EXISTS channel (id integer PRIMARY KEY, channel_id text UNIQUE); "

sql_create_chat_table = """ CREATE TABLE IF NOT EXISTS chat (
                               id integer PRIMARY KEY,
                               channel text NOT NULL,
                               date_time text NOT NULL,
                               sender text NOT NULL,
                               message text NOT NULL,
                               FOREIGN KEY (channel) REFERENCES channel (channel_id)
                           ); """
class DB():

  conn = None
  c = None


  def __init__(self):
    self.conn = sqlite3.connect('strafe-twitch.db', check_same_thread=False)
    self.c = self.conn.cursor()
    self.c.execute("PRAGMA case_sensitive_like=ON;")

    self.create_table(sql_create_channel_table)
    self.create_table(sql_create_chat_table)

  def create_table(self, create_table_sql):
      """
      create a table from the create_table_sql statement

      :param cur: Connection object
      :param create_table_sql: a CREATE TABLE statement
      :return:
      """
      try:
          self.c.execute(create_table_sql)
      except Exception as e:
          print(e)

  def insert_channel(self, channel):
    self.c.execute(f"INSERT INTO channel (channel_id) VALUES ('{channel}')")
    self.conn.commit()

  def insert_message(self, message):
    
    channel = message.channel
    sender = message.sender
    text = message.text

    now = datetime.now().strftime("%b %d %Y %H:%M:%S")

    self.c.execute(
        """
            INSERT INTO chat (channel, sender, message, date_time)
            VALUES (?, ?, ?, ?)
        """,
        [channel, sender, text, now]
    )

    self.conn.commit()
    

  def kappa_per_minute(self, channel):
      """
      Get Kappa per minute count.

      :param channel: Twitch Channel Id
      :return: Counter
      """
      now = datetime.now().strftime("%b %d %Y %H:%M")
      self.c.execute(
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

      return self.c.fetchone()[0]


  def get_msg_count_per_sec(self, channel):
      """
      Get messages per second count

      :param channel: Twitch Channel Id
      :return: Counter
      """
      now = datetime.now().strftime("%b %d %Y %H:%M:%S")
      self.c.execute(
          """
              SELECT COUNT(*)
              FROM
                  chat
              WHERE
                  date_time = ? AND channel = ?;
          """,
          [now, channel]
      )

      return self.c.fetchone()[0]


  def get_msg_count_per_min(self, channel):
    """
    Get messages per minute count

    :param channel: Twitch Channel Id
    :return: Counter
    """
    now = datetime.now().strftime("%b %d %Y %H:%M")
    self.c.execute(
        """
            SELECT COUNT(*)
            FROM
                chat
            WHERE
                date_time LIKE ? AND channel = ?;
        """,
        (f"%{now}%", channel)
    )

    return self.c.fetchone()[0]

  def channel_in_db(self, channel):
    """
    check if channel exists on DB

    :param channel: channel_id
    :return: channel_id OR False
    """
    self.c.execute(f"SELECT channel_id FROM channel WHERE channel_id = '{channel}'")
    r = self.c.fetchone()
    return r[0] if r else False


db = DB()






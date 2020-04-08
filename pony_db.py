from pony.orm import *
from datetime import datetime

db = Database()

class Channel(db.Entity):
    channel_id = Required(str, unique=True)
    chat = Set("Chat")

class Chat(db.Entity):
    channel = Required(Channel)
    date_time = Required(datetime, precision=0)
    sender = Required(str)
    message = Required(str)


# TODO: This code is not respecting the DRY principle
@db_session
def query_message_per_minute(channel):
  print(channel)
  query = Chat.select(lambda m: m.channel.channel_id == channel)
  query_date = query.filter(
      lambda m: m.date_time.date() == datetime.now().date()
  )

  query_time_hour = query_date.filter(
      lambda m: m.date_time.hour == datetime.now().hour
  )

  query_time_minute = query_time_hour.filter(
      lambda m: m.date_time.minute == datetime.now().minute
  ).count()

  return query_time_minute

@db_session
def query_message_per_second(channel):
  print(channel)
  query = Chat.select(lambda m: m.channel.channel_id == channel)
  query_date = query.filter(
      lambda m: m.date_time.date() == datetime.now().date()
  )

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

db.bind(provider='sqlite', filename='database.sqlite', create_db=True)
db.generate_mapping(create_tables=True)

'''
Things to have in mind:

1:
Number of subscribed channels might have to be locked to a limit
depending on hardware capabilities

'''
import twitch
import time
import pickle
from datetime import datetime
import time


CLIENT_ID = 'lnkcgelww2qsqynefsgk487pfuk1wx'
NICKNAME = 'peacewarlando'
OAUTH = 'oauth:q6x6bwve0ea0wnzucnbtxsu9zu5lvy'

# Init Twitch API
helix_api = twitch.Helix(client_id=CLIENT_ID)

msg_stream_per_second = {}
msg_stream_per_minute = {}

def log_message(message):
    global msg_stream_per_second
    global msg_stream_per_minute

    now = datetime.now().strftime("%b %d %Y %H:%M:%S")
    now_min = datetime.now().strftime("%b %d %Y %H:%M")

    if msg_stream_per_second.get(now) == None:
        msg_stream_per_second[now] = 1
    else:
        msg_stream_per_second[now] += 1

    if msg_stream_per_minute.get(now_min) == None:
        msg_stream_per_minute[now_min] = 1
    else:
        msg_stream_per_minute[now_min] += 1

    print("PER SECOND", msg_stream_per_second[now])
    print("PER MINUTE", msg_stream_per_minute[now_min])
    print(message.channel, message.sender, message.text)
        



def channel_exists(channel):
    return helix_api.user(channel)

def track_channel(channel):
    if channel_exists(channel):
        # TODO: Check if channel is already subscribed on DB
        twitch.Chat(channel=f'#{channel}', nickname=NICKNAME, oauth=OAUTH).subscribe(log_message)

    else:
        print("This channel does not exist!")



track_channel("esl_csgo")

from Is_playing import is_playing, is_playing_correct
from random import randrange
from time import sleep
boulevard = '1hwJKpe0BPUsq6UUrwBWTw'


def poll(user):
    while True:
        if is_playing(user) and not is_playing_correct(user):
            user.playback_start_tracks([boulevard])
            user.playback_seek(randrange(50, 200)*1000)
        sleep(1)

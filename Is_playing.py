def is_playing_correct(user):
    current = user.playback_currently_playing()
    return current.item.name == 'Boulevard of Broken Dreams' and current.progress_ms > 100000


def is_playing(user):
    return user.playback().is_playing

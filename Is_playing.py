def is_playing_correct(user):
    current = user.playback_currently_playing()
    if current.item is None:
        return True
    return current.item.name == 'Boulevard of Broken Dreams' and current.progress_ms > 50000


def is_playing(user):
    return user.playback().is_playing

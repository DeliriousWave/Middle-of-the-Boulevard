import tekore as tk

client_id = 'fd2f22d376b146cea9104d032130f655'
client_secret = '94c642a934f14c6aaab4eea568b0a8f5'
redirect_uri = 'https://localhost:5000/callback/'

user_token = tk.prompt_for_user_token(
    client_id,
    client_secret,
    redirect_uri,
    scope=tk.scope.every
)

spotify = tk.Spotify(user_token)

boulevard = '1hwJKpe0BPUsq6UUrwBWTw'
spotify.playback_start_tracks([boulevard])
spotify.playback_seek(140000)
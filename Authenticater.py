import tekore as tk
import os
from flask import Flask, request, redirect, session
os.environ['SPOTIFY_CLIENT_ID'] = 'fd2f22d376b146cea9104d032130f655'
os.environ['SPOTIFY_CLIENT_SECRET'] = '94c642a934f14c6aaab4eea568b0a8f5'
os.environ['SPOTIFY_REDIRECT_URI'] = 'http://localhost:5000/callback/'
conf = tk.config_from_environment()
cred = tk.Credentials(*conf)
spotify = tk.Spotify()
boulevard = '1hwJKpe0BPUsq6UUrwBWTw'

auths = {}  # Ongoing authorisations: state -> UserAuth
users = {}  # User tokens: state -> token (use state as a user ID)

in_link = '<a href="/login">login</a>'
out_link = '<a href="/logout">logout</a>'
login_msg = f'You can {in_link} or {out_link}'


def app_factory() -> Flask:
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '94c642a934f14c6aaab4eea568b0a8f5'

    @app.route('/', methods=['GET'])
    def main():
        user = session.get('user', None)
        token = users.get(user, None)

        # Return early if no login or old session
        if user is None or token is None:
            session.pop('user', None)
            return f'User ID: None<br>{login_msg}'

        page = f'User ID: {user}<br>{login_msg}'
        if token.is_expiring:
            token = cred.refresh(token)
            users[user] = token
        with spotify.token_as(token):
            spotify.playback_start_tracks([boulevard])
            spotify.playback_seek(140000)

        return page

    @app.route('/login', methods=['GET'])
    def login():
        if 'user' in session:
            return redirect('/', 307)

        scope = tk.scope.every
        auth = tk.UserAuth(cred, scope)
        auths[auth.state] = auth
        return redirect(auth.url, 307)

    @app.route('/callback/', methods=['GET'])
    def login_callback():
        code = request.args.get('code', None)
        state = request.args.get('state', None)
        auth = auths.pop(state, None)

        if auth is None:
            return 'Invalid state!', 400

        token = auth.request_token(code, state)
        session['user'] = state
        users[state] = token
        return redirect('/', 307)

    @app.route('/logout', methods=['GET'])
    def logout():
        uid = session.pop('user', None)
        if uid is not None:
            users.pop(uid, None)
        return redirect('/', 307)

    return app


if __name__ == '__main__':
    application = app_factory()
    application.run('127.0.0.1', 5000, threaded=True)

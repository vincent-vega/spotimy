#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from spotify.client import Spotify
from flask import Flask, render_template, redirect, request, make_response, url_for#, session

app = Flask('SpotiMy')
#app.secret_key = b'fowjofi(*ioh(*(*'

@app.route('/', methods=['GET'])
def root_endpoint():
    return render_template('index.html')

@app.route('/list', methods=['GET'])
def login():
    # TODO rename method name and call extern login
    if 'token' in request.cookies:
        data = Spotify.list_playlists(request.cookies.get('token'))
        return render_template('playlists.html', playlists=data['items'])
    print('cookie not found, redirect to spotify...')
    return redirect(Spotify.get_authorize_uri())

def write_cookie(template, cookie: (str, str), age: int=None):
    key, value = cookie
    resp = make_response(template)
    resp.set_cookie(key, value, max_age=age)
    return resp

@app.route('/spotifycb', methods=['GET'])
def spotify_callback():
    authdata = Spotify.token(request.args.get('code'))
    data = Spotify.list_playlists(authdata['access_token'])
    if 'error' in data:
        return write_cookie(render_template('error.html', message=data['error']['message']),
                            ('token', authdata['access_token']),
                            authdata['expires_in'])
    return write_cookie(render_template('playlists.html', playlists=data['items']),
                        ('token', authdata['access_token']),
                        authdata['expires_in'])

@app.route('/save/<playlist_id>', methods=['GET'])
def save_playlist(playlist_id):
    # TODO
    return ''

@app.route('/show/<playlist_id>', methods=['GET'])
def show_playlist(playlist_id):
    if 'token' not in request.cookies:
        return redirect(url_for('login'))
    return render_template('tracks.html', tracks=Spotify.list_track(request.cookies.get('token'), playlist_id))

def main():
    app.config.update(
        DEBUG = True,
        WERKZEUG_DEBUG_PIN = 'off'
    )
    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    main()

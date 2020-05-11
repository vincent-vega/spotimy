#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from spotify.client import Spotify
from flask import Flask, render_template, redirect, request#, session
import base64
import requests

app = Flask('SpotiMy')
#app.secret_key = b'fowjofi(*ioh(*(*'

@app.route('/', methods=['GET'])
def root_endpoint():
    return render_template('index.html')

@app.route('/login', methods=['GET'])
def login():
    return redirect(Spotify.get_authorize_uri())

@app.route('/spotifycb', methods=['GET'])
def spotify_callback():
    authdata = Spotify.token(request.args.get('code'))
    data = Spotify.list_playlists(authdata['access_token'])
    # TODO save access_token in a cookie
    if 'error' in data:
        return render_template('error.html', message=data['error']['message'])
    return render_template('playlists.html', playlists=data['items'])

@app.route('/save/<playlist_id>', methods=['GET'])
def save_playlist(playlist_id):
    # TODO
    pass

def main():
    app.config.update(
        DEBUG = True,
        WERKZEUG_DEBUG_PIN = 'off'
    )
    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, redirect, request#, session
from secrets import client_id, client_secret, redirect_uri
import base64
import requests

app = Flask('SpotiMy')
#app.secret_key = b'fowjofi(*ioh(*(*'

@app.route('/', methods=['GET'])
def root_endpoint():
    return render_template('index.html')

@app.route('/login', methods=['GET'])
def login():
    return redirect(f'https://accounts.spotify.com/authorize?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&scope=playlist-read-private', code=302)

@app.route('/spotifycb', methods=['GET'])
def spotify_callback():
    code = request.args.get('code')
    b64auth = base64.b64encode(bytes(f'{client_id}:{client_secret}', 'utf-8')).decode('utf-8')
    resp = requests.post(f'https://accounts.spotify.com/api/token',
                         data={'grant_type': 'authorization_code', 'code': code, 'redirect_uri': redirect_uri},
                         headers={'Authorization': f'Basic {b64auth}'})
    # TODO error handling
    authdata = resp.json()
    data = list_playlists(authdata['access_token'])
    # TODO save access_token in a cookie
    if 'error' in data:
        return render_template('error.html', message=data['error']['message'])
    return render_template('playlists.html', playlists=data['items'])

@app.route('/save/<playlist_id>', methods=['GET'])
def save_playlist(playlist_id):
    # TODO
    pass

def list_playlists(access_token: str) -> dict:
    resp = requests.get(f'https://api.spotify.com/v1/me/playlists', headers={'Authorization': f'Bearer {access_token}'})
    return resp.json() # TODO check response is json

def main():
    app.config.update(
        DEBUG = True,
        WERKZEUG_DEBUG_PIN = 'off'
    )
    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    main()

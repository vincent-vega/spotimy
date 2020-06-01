#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, redirect, request, make_response, url_for#, session
from spotify.client import Spotify
import json

app = Flask('SpotiMy')
#app.secret_key = b'fowjofi(*ioh(*(*'

@app.route('/login', methods=['GET'])
def login():
    if 'token' in request.cookies:
        return redirect(url_for('show_library'))
    print('cookie not found, redirect to spotify...')
    return redirect(Spotify.get_authorize_uri())

@app.route('/logout', methods=['GET'])
def logout():
    resp = make_response('')
    resp.set_cookie('token', '', expires=0)
    return resp

@app.route('/spotifycb', methods=['GET'])
def spotify_callback():
    authdata = Spotify.token(request.args.get('code'))
    resp = redirect(url_for('show_library'))
    resp.set_cookie('token', authdata['access_token'], max_age=authdata['expires_in'])
    return resp

@app.route('/', methods=['GET'])
@app.route('/library', methods=['GET'])
def show_library():
    if 'token' not in request.cookies:
        return redirect(url_for('login'))
    # TODO corrupted token handling
    data = Spotify.playlists(request.cookies.get('token'))
    return render_template('library.html', playlists=data['items'])

@app.route('/save/<playlist_id>', methods=['GET'])
@app.route('/save/<playlist_id>/<file_name>', methods=['GET'])
def save_playlist(playlist_id: str, file_name: str=None):
    if 'token' not in request.cookies:
        return redirect(url_for('login'))
    tracklist = Spotify.playlist_info(request.cookies.get('token'), playlist_id)
    file_name = tracklist['name'].lower() if file_name is None else file_name
    resp = make_response(json.dumps(tracklist, separators=(',', ':')))
    resp.headers['Content-Disposition'] = f'attachment; filename={file_name}.json'
    resp.headers['Content-type'] = 'application/json'
    return resp

@app.route('/saveliked', methods=['GET'])
def save_liked():
    if 'token' not in request.cookies:
        return redirect(url_for('login'))
    tracklist = Spotify.saved_tracks(request.cookies.get('token'))
    resp = make_response(json.dumps(tracklist, separators=(',', ':')))
    resp.headers['Content-Disposition'] = f'attachment; filename=likedsongs.json'
    resp.headers['Content-type'] = 'application/json'
    return resp

@app.route('/saveall', methods=['GET'])
def save_all():
    if 'token' not in request.cookies:
        return redirect(url_for('login'))
    data = Spotify.playlists(request.cookies.get('token'))
    library = [ Spotify.playlist_info(request.cookies.get('token'), p['id']) for p in data['items'] ]
    library.extend([ Spotify.saved_tracks(request.cookies.get('token')) ])
    resp = make_response(json.dumps(library, separators=(',', ':')))
    resp.headers['Content-Disposition'] = 'attachment; filename=spotimy.json'
    resp.headers['Content-type'] = 'application/json'
    return resp

def _get_track_info(track: dict) -> dict:
    artist = [ artist['name'] for artist in track['track']['artists'] ]
    return { 'artist': artist, 'name': track['track']['name'] }

@app.route('/show/<playlist_id>', methods=['GET'])
def show_playlist(playlist_id: str):
    if 'token' not in request.cookies:
        return redirect(url_for('login'))
    data = Spotify.playlist_info(request.cookies.get('token'), playlist_id)

    try:
        tracks = [ _get_track_info(track) for track in data['tracks']['items'] ]
        return render_template('tracks.html', playlist=tracks)
    except KeyError as e:
        # TODO error handling
        pass

@app.route('/liked', methods=['GET'])
def show_liked():
    if 'token' not in request.cookies:
        return redirect(url_for('login'))
    data = Spotify.saved_tracks(request.cookies.get('token'))

    try:
        tracks = [ _get_track_info(track) for track in data['items'] ]
        return render_template('tracks.html', playlist=tracks)
    except KeyError as e:
        # TODO error handling
        pass

def main():
    app.config.update(
        DEBUG = True,
        WERKZEUG_DEBUG_PIN = 'off'
    )
    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    main()

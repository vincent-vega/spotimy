#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from spotify.secrets import client_id, client_secret, redirect_uri
import base64
import requests

class Spotify:

    @staticmethod
    def get_authorize_uri() -> str:
        return f'https://accounts.spotify.com/authorize?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&scope=playlist-read-private'

    @staticmethod
    def token(code: str) -> dict:
        b64auth = base64.b64encode(bytes(f'{client_id}:{client_secret}', 'utf-8')).decode('utf-8')
        resp = requests.post(f'https://accounts.spotify.com/api/token',
                            data={'grant_type': 'authorization_code', 'code': code, 'redirect_uri': redirect_uri},
                            headers={'Authorization': f'Basic {b64auth}'})
        # TODO error handling
        return resp.json()

    @staticmethod
    def list_playlists(access_token: str) -> dict:
        resp = requests.get(f'https://api.spotify.com/v1/me/playlists',
                            headers={'Authorization': f'Bearer {access_token}'})
        # TODO pagination
        return resp.json() # TODO check response is json

    @staticmethod
    def list_track(access_token: str, playlist_id: str) -> dict:
        resp = requests.get(f'https://api.spotify.com/v1/playlists/{playlist_id}',
                            headers={'Authorization': f'Bearer {access_token}'})
        data = resp.json()
        tracks = [ { 'artist': item['track']['artists'][0]['name'], 'title': item['track']['name'] } for item in data['tracks']['items'] ]
        # TODO pagination, catch key errors, multiple artists
        return tracks
